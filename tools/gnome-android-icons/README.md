# gnome-android-icons (v1.1)

Herhangi bir Android uygulamasının simgesini, uygulamanın kimliğini bozmadan
**gerçek GNOME/Adwaita tarzında** yeniden tasarlayan; düzenlenebilir SVG,
şeffaf PNG (512/256), 3-5 alternatif ve küçük boyut/GNOME karşılaştırma
panosu üreten; ikonu CandyBar ikon paketine güvenli şekilde ekleyen taşınabilir
bir Agent Skill. Görsel üretim modeli **kullanmaz**: her şey kodla yazılmış
SVG ve deterministik araçlarla yapılır.

*English: a portable Agent Skill that redesigns any Android app icon as a
GNOME/Adwaita-style icon (editable SVG + transparent PNG + 3-5 alternatives +
review boards) and adds it safely to a CandyBar icon pack. No generative image
tools. Start with `SKILL.md`.*

## Kurulum

Klasörün **tamamını** kopyalayın (yalnızca SKILL.md yetmez: referans SVG'ler,
scriptler ve belgeler klasörün içinde).

| Ajan | Kişisel (tüm projeler) | Proje içi (ikon paketi reposu) |
|---|---|---|
| Claude Code | `~/.claude/skills/gnome-android-icons/` | `<repo>/.claude/skills/gnome-android-icons/` |
| Codex | `~/.agents/skills/gnome-android-icons/` | `<repo>/.agents/skills/gnome-android-icons/` |
| OpenCode | `~/.config/opencode/skills/...` (ayrıca `~/.claude/skills`, `~/.agents/skills` okur) | `<repo>/.opencode/skills/...` veya `.claude/skills` / `.agents/skills` |

İkon paketi reposunda tek kopya için öneri: `<repo>/.agents/skills/gnome-android-icons/`
(Codex + OpenCode okur) ve Claude Code için bir bağlantı:
`mkdir -p .claude/skills && ln -s ../../.agents/skills/gnome-android-icons .claude/skills/gnome-android-icons`
(Windows'ta bağlantı yerine kopyalayın).

Python bağımlılıkları (bir kez) ve ortam kontrolü:

```bash
python3 -m pip install -r requirements.txt     # PEP 668 sistemlerde: --break-system-packages veya venv
python3 scripts/doctor.py                      # eksik bir şey varsa nasıl kurulacağını söyler
```

İsteğe bağlı: `adb` (telefondan gerçek ComponentInfo ve APK almak için),
MoreWaita / Adwaita++ arşivlerinizin yolu:
`export GNOME_ICONS_MOREWAITA=~/arsiv/MoreWaita-main.zip GNOME_ICONS_ADWAITAPP=~/arsiv/adwaita-plus-master.zip`

## v1.1'de yeni olanlar

- **Tek komutla başlangıç:** `new_icon.py` artık ekran görüntüsü / PNG, SVG, VectorDrawable XML ve APK kabul ediyor; gerçek geometriyi çıkarıp her alternatif için GNOME yapısında **taslaklar** üretiyor, inceleme ve okunabilirlik panolarını çiziyor. Taslaklar başlangıç noktasıdır, bitmiş tasarım değildir.
- **Okunabilirlik testi (`legibility_check.py`):** 32/48 px'de kaynaşacak boşlukları (kırmızı) ve kaybolacak ince parçaları (turuncu) işaretler; resmî GNOME simgelerinin değerleriyle karşılaştırır.
- **Launcher önizlemesi (`launcher_preview.py`):** telefon ana ekranında gerçek boyut (54 dp ≈ 149 px), açık / koyu / renkli duvar kâğıdı ve launcher'ların simgeyi daire/squircle içine zorladığı durum.
- **Paket denetimi (`pack_audit.py`):** CandyBar projesinde eksik çizimler, çift eşlemeler, bozuk ComponentInfo, senkron olmayan XML kopyaları, yetim PNG'ler ve görsel ağırlığı aileden sapan simgeler.
- **Renk taraması (`recolor.py`):** aynı simgeyi 7 GNOME renk ailesinde üretir (rengi olmayan logolar için).
- **SVG düzleştirme (`flatten_svg.py`):** herhangi bir SVG'yi dönüşümleri uygulanmış, çizgileri dolguya çevrilmiş saf geometriye çevirir.
- **Daha iyi izleme (`trace_source.py`):** gradyanlı simgeler artık renk bantlarına bölünmüyor (tek parça + gradyan durakları; taslaklar gradyanı GNOME tarzında yeniden kuruyor); göz parlaması, yanak, susam gibi küçük ayrıntılar geri getiriliyor; yakalanamayan ayrıntılar `brief.md`'de konumlarıyla listeleniyor.
- **Daha iyi ayıklama (`extract_icon.py`):** beyaz/gri zemin üzerindeki simge (web'den kaydedilmiş JPEG gibi) artık yanlışlıkla bir şerit olarak kesilmiyor; zemin kaldırılıp köşeler şeffaf yapılıyor.
- Çizim kütüphanesine çok parçalı işaretler (`pieces`, `glyphs`), otomatik yerleştirme (`fit_parts`) ve koyu/açık zeminlere uygun alt şerit renkleri eklendi; inceleme panosundaki referanslar artık isimli.

## Kullanım örnekleri (ajana yazılacak)

- *"gnome-android-icons skill'ini kullan: ekteki ekran görüntüsündeki uygulamanın simgesini GNOME tarzına çevir, 3 alternatif yap, karşılaştırma panosunu göster."*
- *"Telefon USB'de bağlı. `org.example.app` paketinin APK'sından gerçek vektörü al, simgeyi dönüştür, CandyBar projeme 'Sosyal' kategorisine ekle (önce dry-run göster)."*
- Codex'te açıkça çağırmak için: `$gnome-android-icons ...`

## İçerik

- `SKILL.md` - ajanın izlediği kurallar ve iş akışı
- `references/` - ölçülmüş GNOME stil rehberi, arketipler, alternatif sistemi, kimlik koruma, geçmiş dersler, inceleme protokolü, CandyBar, topluluk temaları, SVG yapımı, kaynaklar, kullanıcı gereksinimleri (TR)
- `assets/reference-library/` - 134 gerçek, değiştirilmemiş GNOME referans SVG'si + `catalog.json` (kaynak repo, commit, lisans, ölçümler) + kontakt sayfaları
- `assets/template/` - GNOME HIG şablonu ve 45 renkli palet
- `scripts/` - 23 araç (ayıklama, analiz, potrace izleme, SVG düzleştirme, APK vektörü, taslak üretimi, gnome_kit, renk taraması, lint, ölçüm, okunabilirlik, inceleme panosu, launcher önizlemesi, paket denetimi, PNG, CandyBar, ortam kontrolü)
- `examples/demo-original-apps/` - 3 uydurma uygulama (Martı, Lale, Simit) için kaynak logo + 11 GNOME alternatifi, PNG'ler, inceleme, okunabilirlik ve launcher panoları
- `tests/` - `python3 -m unittest discover -s tests -v`

## Dürüstlük notları

- Teknik testlerin geçmesi tasarımın iyi olduğunu kanıtlamaz; her tasarım inceleme panosuyla gözle kontrol edilir ve onayı kullanıcı verir.
- `apk_icon.py` ve `new_icon.py`'nin `.apk` yolu gerçek APK'larla (androguard'ın test APK'ları: vektör adaptive ikonlar, derlenmiş gradyanlar, yalnızca bitmap olan ikonlar) denendi. Karartılmış (obfuscated) ya da alışılmadık kaynak tablolarında yine başarısız olabilir; o zaman script neyi çözemediğini söyler.
- Okunabilirlik sayıları (SSIM, boşluk sayısı) ve görsel ağırlık bandı yönlendiricidir; ince ama hafif bir simge yüksek SSIM alıp yine de zayıf görünebilir. Karar her zaman panolara bakılarak verilir.
- `find_component.py --adb` ve CandyBar projesinin Gradle derlemesi bu ortamda (telefon/Android SDK olmadığı için) çalıştırılmadı; `candybar_add.py` resmi CandyBar örnek projesinin bir kopyası üzerinde test edildi.
- MoreWaita / Adwaita++ dosyaları pakete konmadı (marka türevi, GPL); scriptler kendi arşivlerinizden okur.
