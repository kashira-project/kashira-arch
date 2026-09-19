#!/usr/bin/env python3
"""kashira-arch sync tool.

Vendors Arch Linux packaging repos (gitlab.archlinux.org) into upstream/,
applies kashira deltas from delta/, and materializes buildable trees in pkgs/.

Layout:
  upstream/<pkgbase>/        verbatim Arch files (+ .arch-ref marker)
  delta/<pkgbase>/files/     overlaid verbatim after copy (full-file replace/add)
  delta/<pkgbase>/patches/   *.patch applied with patch -p1 on the materialized tree
  pkgs/<pkgbase>/            materialized = upstream + delta (what makepkg sees)
  tools/tracked.tsv          pkgbase <TAB> origin(fork-vanilla|fork-delta)
  tools/denylist.txt         pkgbases owned by kashira-pkgs; never vendored

Commands:
  sync [pkgbase...]     fetch/update upstream, re-materialize (all tracked if no args)
  import <pkgbase>      onboard a new Arch package as fork-vanilla, then sync it
  materialize [pb...]   regenerate pkgs/ from upstream/ + delta/ without fetching
  status                show tracked pkgbases whose upstream HEAD moved
"""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITLAB = "https://gitlab.archlinux.org/archlinux/packaging/packages/{}.git"
CACHE = os.path.join(ROOT, ".cache")


def read_list(path):
    with open(path) as f:
        return [l.split("#")[0].strip() for l in f if l.split("#")[0].strip()]


def tracked():
    out = {}
    for line in read_list(os.path.join(ROOT, "tools", "tracked.tsv")):
        name, origin = line.split("\t")
        out[name] = origin
    return out


def run(cmd, **kw):
    kw.setdefault("timeout", 120)  # GitLab rate-limits; never hang forever
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def head_sha(pkgbase):
    r = run(["git", "ls-remote", GITLAB.format(pkgbase), "refs/heads/main"])
    return r.stdout.split()[0]


def vendored_ref(pkgbase):
    p = os.path.join(ROOT, "upstream", pkgbase, ".arch-ref")
    return open(p).read().strip() if os.path.exists(p) else None


def fetch(pkgbase):
    """Clone/update the cache repo, return its HEAD sha."""
    dest = os.path.join(CACHE, pkgbase)
    if os.path.isdir(dest):
        run(["git", "-C", dest, "fetch", "--depth", "1", "origin", "main"])
        run(["git", "-C", dest, "reset", "--hard", "FETCH_HEAD"])
    else:
        run(["git", "clone", "--depth", "1", GITLAB.format(pkgbase), dest])
    return run(["git", "-C", dest, "rev-parse", "HEAD"]).stdout.strip()


def vendor(pkgbase):
    sha = fetch(pkgbase)
    src = os.path.join(CACHE, pkgbase)
    dst = os.path.join(ROOT, "upstream", pkgbase)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git"))
    with open(os.path.join(dst, ".arch-ref"), "w") as f:
        f.write(sha + "\n")
    return sha


def materialize(pkgbase):
    src = os.path.join(ROOT, "upstream", pkgbase)
    dst = os.path.join(ROOT, "pkgs", pkgbase)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".arch-ref"))
    dfiles = os.path.join(ROOT, "delta", pkgbase, "files")
    if os.path.isdir(dfiles):
        shutil.copytree(dfiles, dst, dirs_exist_ok=True)
    dpatches = os.path.join(ROOT, "delta", pkgbase, "patches")
    if os.path.isdir(dpatches):
        for patch in sorted(os.listdir(dpatches)):
            if not patch.endswith(".patch"):
                continue
            r = subprocess.run(
                ["patch", "-p1", "--no-backup-if-mismatch", "-d", dst,
                 "-i", os.path.join(dpatches, patch)],
                capture_output=True, text=True)
            if r.returncode != 0:
                print(f"DELTA-CONFLICT {pkgbase}: {patch}\n{r.stdout}{r.stderr}",
                      file=sys.stderr)
                return False
    return True


def cmd_sync(names):
    t = tracked()
    names = names or sorted(t)
    changed, failed = [], []
    def one(name):
        if name not in t:
            return (name, "not tracked")
        try:
            remote = head_sha(name)
            if remote == vendored_ref(name):
                return (name, None)
            sha = vendor(name)
            return (name, sha)
        except subprocess.CalledProcessError as e:
            return (name, "error: " + (e.stderr or "").strip()[:200])
    with ThreadPoolExecutor(8) as ex:
        for name, result in ex.map(one, names):
            if result is None:
                continue
            if result.startswith(("error", "not tracked")):
                failed.append((name, result))
                print(f"FAIL {name}: {result}", file=sys.stderr)
            else:
                changed.append(name)
                print(f"vendored {name} @ {result[:12]}")
    bad = [n for n in changed if not materialize(n)]
    print(f"sync: {len(changed)} updated, {len(names) - len(changed) - len(failed)} unchanged, "
          f"{len(failed)} fetch-failed, {len(bad)} delta-conflicts")
    return 1 if (failed or bad) else 0


def cmd_import(pkgbase):
    deny = set(read_list(os.path.join(ROOT, "tools", "denylist.txt")))
    if pkgbase in deny:
        sys.exit(f"{pkgbase} is denylisted: owned by kashira-pkgs (the heart repo)")
    t = tracked()
    if pkgbase in t:
        sys.exit(f"{pkgbase} already tracked ({t[pkgbase]})")
    head_sha(pkgbase)  # fails if the repo does not exist
    with open(os.path.join(ROOT, "tools", "tracked.tsv"), "a") as f:
        f.write(f"{pkgbase}\tfork-vanilla\n")
    return cmd_sync([pkgbase])


def cmd_status():
    stale = []
    for name in sorted(tracked()):
        try:
            remote = head_sha(name)
        except subprocess.CalledProcessError:
            print(f"{name}: upstream fetch failed", file=sys.stderr)
            continue
        if remote != vendored_ref(name):
            stale.append(name)
            print(f"{name}: upstream moved")
    print(f"{len(stale)} stale")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd, args = sys.argv[1], sys.argv[2:]
    os.makedirs(CACHE, exist_ok=True)
    if cmd == "sync":
        return cmd_sync(args)
    if cmd == "import":
        if len(args) != 1:
            sys.exit("usage: sync.py import <pkgbase>")
        return cmd_import(args[0])
    if cmd == "materialize":
        names = args or sorted(tracked())
        bad = [n for n in names if not materialize(n)]
        print(f"materialize: {len(names) - len(bad)} ok, {len(bad)} delta-conflicts")
        return 1 if bad else 0
    if cmd == "status":
        return cmd_status()
    sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    sys.exit(main())
