# Maintainer: Balló György <ballogyor+arch at gmail dot com>
# Contributor: Jan de Groot <jgc@archlinux.org>
# Contributor: tardo <tardo@nagi-fanboi.net>
# Contributor: William Rea <sillywilly@gmail.com>

pkgname=mod_dnssd
pkgver=0.6
pkgrel=10
pkgdesc='Zeroconf module for Apache'
arch=(x86_64)
url='https://0pointer.de/lennart/projects/mod_dnssd/'
license=(Apache-2.0)
depends=(
  apache
  apr
  avahi
  glibc
)
source=(
  "http://0pointer.de/lennart/projects/$pkgname/$pkgname-$pkgver.tar.gz"
  fix_undefined_reference.patch
)
b2sums=(
  01aee3624e413f5a00d6e63e5e74d9dc1667db9e9747b65a7fce9ab762cf0f9a5cd3ef4dcccf9532e9aa70435bd6afd846fdbaafff6667ba1fd9d413ea6fe0d9
  aa89b74651a656f9520aa99e7bd25bd8929675a40ea1630834208038be268eb4987535539ac2a1e337e3535efad216a0fa35cf5c35d88c1a7d290d411093c0f7
)

prepare() {
  cd $pkgname-$pkgver

  # http://git.0pointer.net/mod_dnssd.git/commit/?id=be2fb9f6158f800685de7a1bc01c39b6cf1fa12c
  patch -Np1 -i ../fix_undefined_reference.patch

  autoreconf -fiv
}

build() {
  cd $pkgname-$pkgver
  ./configure \
    --prefix=/usr \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --disable-lynx
  make
}

package() {
  cd $pkgname-$pkgver
  install -Dm755 src/.libs/mod_dnssd.so "$pkgdir/usr/lib/httpd/modules/mod_dnssd.so"
}
