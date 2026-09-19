# Maintainer: George Rawlinson <grawlinson@archlinux.org>

pkgname=python-vcs-versioning
pkgver=2.4.1
pkgrel=1
pkgdesc='the blessed package to manage your versions by vcs metadata'
arch=(any)
url='https://github.com/pypa/setuptools-scm'
license=(MIT)
depends=(
  python
  python-packaging
  python-setuptools
)
makedepends=(
  git
  python-build
  python-installer
)
checkdepends=(
  python-pytest
  python-pytest-timeout
  python-setuptools-scm
  jujutsu
  mercurial
)
optdepends=('python-rich: formatting of log messages')
source=("python-setuptools-scm::git+$url#tag=vcs-versioning-v$pkgver")
sha512sums=('37fac968a911aae33ec44fa125e1e98637d8dc1216ec78d724bde0e3f37cae95a2cd2d9ee718eb59a3f029fc5f6f6247e2772ea21bbf3dbd4ad054b69461d358')
b2sums=('3c397fb7030e49a5318cfe32f040caeb4b8ec192e5cffecd714815ce6c62d5e92a5ffc902460c4ce89d7ec97f0690464935eb92c48c92cd0db8e6c3f9b80f7f4')

build() {
  cd python-setuptools-scm/vcs-versioning

  python -m build --wheel --no-isolation
}

check() {
  cd python-setuptools-scm/vcs-versioning

  # temporary install
  python -m installer --destdir="$(pwd)/tmp" dist/*.whl
  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
  export PYTHONPATH="$(pwd)/tmp/$site_packages"

  local pytest_options=(
    -vv
    --deselect testing_vcs/test_jj.py::test_jj_disable_jj_falls_back_to_git
  )

  pytest "${pytest_options[@]}"
}

package() {
  cd python-setuptools-scm/vcs-versioning

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE.txt
}
