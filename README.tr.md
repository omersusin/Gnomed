<h1 align="center">Gnomed</h1>

<p align="center"><b>Android için GNOME / Adwaita uygulama simgeleri.</b><br>
Her uygulama bir GNOME nesnesi olarak yeniden çizilir: basit şekiller, GNOME paleti, yukarıdan gelen ışık.</p>

<p align="center">
  <a href="https://github.com/omersusin/Gnomed/releases/latest"><img alt="Son sürüm" src="https://img.shields.io/github/v/release/omersusin/Gnomed?label=s%C3%BCr%C3%BCm&labelColor=3d3846&color=3584e4&style=for-the-badge"></a>
  <a href="https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/%7B%22id%22%3A%22gnomed.it%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2Fomersusin%2FGnomed%22%2C%22author%22%3A%22omersusin%22%2C%22name%22%3A%22Gnomed%22%2C%22preferredApkIndex%22%3A0%2C%22additionalSettings%22%3A%22%7B%5C%22apkFilterRegEx%5C%22%3A%5C%22gnomed-symbol%5C%5C%5C%5C.apk%5C%22%2C%5C%22appName%5C%22%3A%5C%22Gnomed%5C%22%2C%5C%22appAuthor%5C%22%3A%5C%22omersusin%5C%22%7D%22%2C%22overrideSource%22%3Anull%7D"><img alt="Obtainium ile al" src="https://img.shields.io/static/v1?label=&message=Obtainium&labelColor=613583&color=9141ac&logo=obtainium&logoColor=ffffff&style=for-the-badge"></a>
</p>

<p align="center">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/1.jpg" width="200" alt="Symbol">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/2.jpg" width="200" alt="Faithful">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/3.jpg" width="200" alt="Disc">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/4.jpg" width="200" alt="Rimmed">
</p>

> **English:** [README.md](README.md)

## Kurulum

1. [Son sürümden](https://github.com/omersusin/Gnomed/releases/latest) **`gnomed-symbol.apk`** dosyasını
   indir — ya da güncellemeleri kendiliğinden almak için yukarıdaki **Obtainium** düğmesine dokun.
2. Gnomed'i aç → **Uygula** → başlatıcını seç.
3. Başka bir görünüm mü istiyorsun? Gnomed → menü → **Simge stili**. Uygulama o stilin APK'sını
   indirir ve kendi güncellemesi olarak kurar (aynı uygulama, aynı ayarlar).

CandyBar'ın desteklediği başlatıcılarla çalışır: Nova, Lawnchair, Niagara, Smart Launcher,
Hyperion, Kvaesitso, KISS, Action, Apex ve dahası.

## Dört stil

<p align="center"><img src="docs/images/styles.png" width="760" alt="Dört Gnomed stili"></p>

| Stil | Ne |
|---|---|
| **Symbol** | asıl Gnomed tasarımı: uygulamanın fikri bir GNOME nesnesi olarak (önerilen) |
| **Faithful** | orijinal logoya en yakın tasarım |
| **Disc** | yuvarlak bir tasarım |
| **Rimmed** | aynı uygulamanın başka bir tasarımı |

## Bütün simgeler

<p align="center"><img src="docs/images/preview.png" width="760" alt="Symbol stilindeki bütün simgeler"></p>

**Dürüst durum:** Gnomed yeni. Resmin sol üstündeki simgeler (Telegram, Pokémon UNITE, Rush
Royale, Aurex Browser, Horus, AnDVM) Gnomed yöntemiyle yeniden çizildi; diğerleri ilk sürümler ve
tek tek yenileniyor — [docs/ROADMAP.md](docs/ROADMAP.md), uygulama listesi [docs/APPS.md](docs/APPS.md).

## Bir uygulama mı eksik?

Gnomed'de **İstek** ekranını aç, uygulamaları seç, gönder. Ya da bir
[**Icon request**](https://github.com/omersusin/Gnomed/issues/new/choose) kaydı aç. Bir simge bozuk
mu? [**Icon problem**](https://github.com/omersusin/Gnomed/issues/new/choose).

## Katkı

- Çizen insanlar: [CONTRIBUTING.md](CONTRIBUTING.md) (İngilizce) · [şablon](docs/template/gnomed-template.svg) · [palet](docs/palette/)
- Yapay zekâ ajanları: [START-HERE.md](START-HERE.md) → `python3 tools/next.py <uygulama>`
- Tasarım kuralları: [REDESIGN.md](REDESIGN.md) · [docs/RESEARCH.md](docs/RESEARCH.md)

`main` dalına yalnızca proje sahibi dokunur; herkes bir dalda çalışır ve pull request açar.
Görsel üretim aracı kullanılmaz: her simge vektör çizimdir (Python → SVG → PNG).

## Lisans

Kod ve simgeler [GPL-3.0](LICENSE). Uygulama adları, logolar ve markalar sahiplerine aittir;
Gnomed onları yalnızca kişisel tema için çizer, onlarla ya da GNOME ile bağlantılı değildir.
