# Maintainer: Robin Candau <antiz@archlinux.org>
# Contributor: Morten Linderud <foxboron@archlinux.org>

pkgname=sbctl
pkgver=0.18
pkgrel=2
pkgdesc="Secure Boot key manager"
url="https://github.com/Foxboron/sbctl"
arch=('x86_64')
license=('MIT')
depends=('binutils' 'util-linux' 'pcsclite')
makedepends=('go' 'git' 'asciidoc')
source=("git+${url}.git#tag=${pkgver}?signed")
validpgpkeys=("C100346676634E80C940FB9E9C02FF419FECBE16")
sha256sums=('b40f21c8137a908f3f9aba14a7b94234e84587f02b503a09e0bbcf09e4ad14a3')

build(){
	cd "${pkgname}"
	export GOFLAGS="-buildmode=pie -trimpath -modcacherw"
	make
}

package(){
	cd "${pkgname}"
	make PREFIX="${pkgdir}/usr" install
	install -Dm 644 contrib/pacman/ZZ-sbctl.hook "${pkgdir}/usr/share/libalpm/hooks/zz-sbctl.hook"
	install -Dm 755 contrib/mkinitcpio/sbctl "${pkgdir}/usr/lib/initcpio/post/sbctl"
}
