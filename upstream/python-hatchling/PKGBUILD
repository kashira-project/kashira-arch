# Maintainer: Santiago Torres-Arias <santiago @ usualplace>
# Maintainer: Carl Smedstad <carsme@archlinux.org>
# Contributor: Kaizhao Zhang <zhangkaizhao@gmail.com>

pkgname=python-hatchling
pkgver=1.32.0
pkgrel=1
pkgdesc="Extensible, standards compliant build backend used by Hatch"
arch=('any')
url="https://github.com/pypa/hatch/tree/master/backend"
license=('MIT')
groups=(python-build-backend)
depends=(
  'python'
  'python-editables'
  'python-packaging'
  'python-pathspec'
  'python-pluggy'
  'python-tomlkit'
  'python-trove-classifiers'
)
makedepends=(
  'python-build'
  'python-installer'
)
checkdepends=(
  'libxcrypt-compat'
  'python-click'
  'python-filelock'
  'python-hatch-vcs'
  'python-pytest'
  'python-rich'
  'python-tomli-w'
  'python-uv'
)
source=("https://github.com/pypa/hatch/archive/hatchling-v$pkgver.tar.gz")
b2sums=('a3eea27c39600ccf7b45e1b8de28112f3b92380f80579049013101cefde5f734225d71ac330d1b76a6c39c8f2e4a6e8b116f548b5eab305852a71d6d0b6c0094')

build() {
  cd hatch-hatchling-v$pkgver
  python -m build --wheel --no-isolation backend
}

check() {
  cd hatch-hatchling-v$pkgver
  python -m venv --system-site-packages test-env
  test-env/bin/python -m installer backend/dist/*.whl

  # The tests for hatchling depend on hatch - build and install it to the test
  # environment.
  test-env/bin/python -m build --wheel --no-isolation --skip-dependency-check
  test-env/bin/python -m installer dist/*.whl

  SOURCE_DATE_EPOCH=1580601600 test-env/bin/python -m pytest tests/backend
}

package() {
  cd hatch-hatchling-v$pkgver
  python -m installer --destdir="$pkgdir" backend/dist/*.whl
  install -vDm644 -t "$pkgdir/usr/share/doc/$pkgname" backend/README.md
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" backend/LICENSE.txt
}
