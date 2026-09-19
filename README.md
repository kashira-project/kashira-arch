# kashira-arch — vendored Arch Linux forks

Arch Linux PKGBUILDs tracked from upstream, carrying minimal kashira deltas.
Companion to [kashira-pkgs](https://github.com/kashira-project/kashira-pkgs)
(the heart: toolchain, replacements, distro identity). Plan:
`planning/repo-structure.md` in the kashira repo.

## Layout

- `upstream/<pkgbase>/` — verbatim Arch packaging tree (`+ .arch-ref` marker)
- `delta/<pkgbase>/files/` — full-file overlay
- `delta/<pkgbase>/patches/` — `patch -p1` series, applied in name order
- `pkgs/<pkgbase>/` — materialized build tree (upstream + delta); what makepkg sees
- `tools/tracked.tsv` — pkgbase + origin (fork-vanilla / fork-delta)
- `tools/denylist.txt` — roles owned by kashira-pkgs; sync refuses these
- `tools/name-map.tsv` — historical kashira-name → Arch pkgbase correlations

## Usage

```sh
tools/sync.py  sync            # update all tracked packages from Arch
tools/sync.py  import <pkg>    # onboard a new Arch package (fork-vanilla)
tools/sync.py  materialize     # regenerate pkgs/ after editing a delta
tools/sync.py  status          # which upstreams moved
```

## Delta rules

- fork-vanilla: zero delta. If a build breaks under our clang/lld/openssl-4
  environment and can't be fixed globally in makepkg.conf, it graduates to
  fork-delta with a minimal, commented patch.
- A delta that stops applying = sync conflict = human review. Deltas must
  never silently drop: fakeroot's no-latch patch is load-bearing for every
  makepkg run under our glibc malloc-selector patchset.
- Pinned-ahead: when kashira deliberately tracks a NEWER upstream than
  Arch (openssl-style policy; today: perl, shadow, iana-etc), the delta is
  a full-recipe overlay (`files/PKGBUILD` + companions) marked with a
  `PINNED-AHEAD` note. `sync.py status` still tracks Arch; when Arch
  reaches our version, drop the overlay.
- Upstream is truth for versions and features, except pinned-ahead
  packages. kashira policy lives in makepkg.conf and kashira-pkgs, not
  here.
