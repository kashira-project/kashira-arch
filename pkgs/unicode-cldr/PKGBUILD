# Maintainer: Felix Yan <felixonmars@archlinux.org>

shopt -s extglob

pkgbase=unicode-cldr
pkgname=(unicode-cldr unicode-cldr-annotations)
pkgver=48.2
pkgrel=1
pkgdesc="Unicode Common Locale Data Repository"
arch=('any')
url="http://cldr.unicode.org/"
license=('Unicode-3.0')
source=("https://unicode.org/Public/cldr/$pkgver/cldr-common-$pkgver.zip")
sha512sums=('de8660f5371e0fcfd03a42e3b4fc4c686ec6cd602b402f1e3d227844005a54eb7952873894443523837d5828c42874a1a267a19f91ded207a2d166144791fa62')

package_unicode-cldr-annotations() {
  pkgdesc="Unicode Common Locale Data Repository (annotations only)"

  cd common
  install -dm755 "$pkgdir"/usr/share/unicode/cldr/common
  cp -r annotations "$pkgdir"/usr/share/unicode/cldr/common/
  install -Dm644 ../LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}

package_unicode-cldr() {
  depends=('unicode-cldr-annotations')

  cd common
  install -dm755 "$pkgdir"/usr/share/unicode/cldr/common
  cp -r !(annotations) "$pkgdir"/usr/share/unicode/cldr/common/

  install -Dm644 ../LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname/
}
