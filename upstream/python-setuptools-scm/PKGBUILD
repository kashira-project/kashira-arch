# Maintainer: Felix Yan <felixonmars@archlinux.org>
# Maintainer: Daniel M. Capella <polyzen@archlinux.org>
# Contributor: Hugo Osvaldo Barrera <hugo@barrera.io>

pkgname=python-setuptools-scm
pkgver=10.3.3
pkgrel=1
pkgdesc='Handles managing your python package versions in scm metadata'
arch=(any)
url=https://github.com/pypa/setuptools-scm
license=(MIT)
depends=(
  python
  python-packaging
  python-setuptools
  python-vcs-versioning
)
makedepends=(
  git
  python-build
  python-installer
  python-wheel
)
checkdepends=(
  mercurial
  python-pip
  python-pytest
  python-pytest-timeout
  python-rich
)
checkdepends_riscv64=(
  libxml2
  libxslt
)
optdepends=(
  'python-rich: use rich as console log handler'
)
source=("$pkgname::git+$url.git#tag=setuptools-scm-v$pkgver")
sha512sums=('37fac968a911aae33ec44fa125e1e98637d8dc1216ec78d724bde0e3f37cae95a2cd2d9ee718eb59a3f029fc5f6f6247e2772ea21bbf3dbd4ad054b69461d358')
b2sums=('3c397fb7030e49a5318cfe32f040caeb4b8ec192e5cffecd714815ce6c62d5e92a5ffc902460c4ce89d7ec97f0690464935eb92c48c92cd0db8e6c3f9b80f7f4')

build() {
  cd "$pkgname/setuptools-scm"
  python -m build --wheel --skip-dependency-check --no-isolation
}

check() {
  cd "$pkgname/setuptools-scm"

  # temporary install
  python -m installer --destdir="$(pwd)/tmp" dist/*.whl
  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
  export PYTHONPATH="$(pwd)/tmp/$site_packages"

  local pytest_opts=(
    -v
    -k 'not test_not_owner'
    --deselect testing_scm/test_basic_api.py::test_get_version_blank_tag_regex
    --deselect testing_scm/test_integration.py::test_setuptools_version_keyword_ensures_regex
    --deselect "testing_scm/test_integration.py::test_commands_registered_only_when_inference_produced_data[not-configured]"
    --deselect "testing_scm/test_integration.py::test_commands_registered_only_when_inference_produced_data[version-already-set]"
  )

  pytest "${pytest_opts[@]}"
}

package() {
  cd "$pkgname/setuptools-scm"

  python -m installer --destdir="$pkgdir" dist/*.whl

  # license
  install -vDm644 -t "$pkgdir/usr/share/licenses/$pkgname" LICENSE
}
