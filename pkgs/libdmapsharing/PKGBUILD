# Maintainer: Jan Alexander Steffens (heftig) <heftig@archlinux.org>
# Contributor: Ionut Biru <ibiru@archlinux.org>

pkgname=libdmapsharing
pkgver=3.9.14
pkgrel=1
pkgdesc="A library that implements the DMAP family of protocols"
url="https://www.flyn.org/projects/libdmapsharing/index.html"
arch=(x86_64)
license=(LGPL-2.1-or-later)
depends=(
  avahi
  gdk-pixbuf2
  glib2
  glibc
  gst-plugins-base-libs
  gstreamer
  libsoup3
  zlib
)
makedepends=(
  git
  glib2-devel
  gobject-introspection
  gtk-doc
  vala
)
provides=(libdmapsharing-4.0.so)
source=("git+https://gitlab.gnome.org/GNOME/libdmapsharing.git#tag=LIBDMAPSHARING_${pkgver//./_}")
b2sums=('890c3f9dcd2a06443897be164a36b266a44629d58bd68e48d0518bdd52f8d55f4d45465053c1b567204f8851a11dde1899f568529ba39b4899eb94a0d77bbc93')

prepare() {
  cd $pkgname
  NOCONFIGURE=1 ./autogen.sh
}

build() {
  local configure_args=(
    --prefix=/usr
    --sysconfdir=/etc
    --localstatedir=/var
    --with-mdns=avahi

    # Disable tests; get built into the library, adding a dep on libcheck
    --disable-tests

    # GTK-docs are broken when tests are disabled
    --disable-gtk-doc
  )


  cd $pkgname
  ./configure "${configure_args[@]}"
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
  make
}

package() {
  cd $pkgname
  make DESTDIR="$pkgdir" install
}

# vim:set sw=2 sts=-1 et:
