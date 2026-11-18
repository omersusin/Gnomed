# GNOME / Adwaita Android Icon Pack — Claude Handoff

**Proje türü:** Android ikon paketi + farklı kod ajanlarında kullanılabilecek taşınabilir tasarım/üretim skill'i  
**Mevcut skill adı:** `gnome-android-icons`  
**Son mevcut sürüm:** v0.9 (nihai veya görsel kalitesi onaylanmış sürüm değil)  
**Dil:** Türkçe iletişim; skill ve kod dosyaları teknik gereksinime göre İngilizce olabilir.

## 1. Ben ne yapmak istiyorum?

GNOME'un uygulama simgelerini, tasarım felsefesini ve Adwaita görsel dilini çok seviyorum. Bu görünümü Android telefonumda kullanabileceğim **kapsamlı bir ikon paketine** dönüştürmek istiyorum.

Tek tek simgeleri hazırlamak için her defasında tasarımı yeniden açıklamak istemiyorum. Bu nedenle **Claude Code, Codex, OpenCode ve benzeri kod ajanlarında çalışabilecek yeniden kullanılabilir bir skill** istiyorum. Ben dönüştürmek istediğim uygulamanın logosunu, ikonunu veya ekran görüntüsünü verdiğimde skill, uygulamanın görsel kimliğini koruyarak gerçek GNOME/Adwaita estetiğine uygun bir ikon oluşturmalı. Ardından bu ikonu Android ikon paketi projemin içine ekleyebilmeliyim.

İkon paketinin uygulama tarafında **CandyBar veya benzeri bir icon-pack dashboard** kullanmayı düşünüyorum. Dashboard/framework konusunda kesinleşmiş tek bir seçimim yok; amaç ikonların Android launcher'larında kullanılabilir olması.

**Kapsam yalnızca Firefox değil.** Sosyal medya, tarayıcı, müzik, video, oyun, mesajlaşma, araçlar, geliştirici uygulamaları, belgeler, marka sembolleri ve maskot içeren uygulamalar dahil her türlü uygulama için aynı kaliteyi istiyorum.

## 2. Değişmez kurallarım

1. **ImageGen, DALL·E, Stable Diffusion veya başka herhangi bir üretken görsel oluşturma/düzenleme aracı kesinlikle kullanılmayacak.** Önceki çalışmalarda bu yasağım defalarca ihlal edildi; tekrar edilmesini istemiyorum.
2. **Yalnızca gerçek SVG/vector kaynaklar, doğrudan SVG çizimi ve kod tabanlı araçlar** kullanılacak. Inkscape, CairoSVG, Pillow, Python, SVG/XML işleme, kaynak kontur analizi ve PNG dışa aktarma uygundur.
3. Bir PNG'yi SVG içine `<image>` olarak koyup "düzenlenebilir vektör" diye sunmak istemiyorum. Nihai tasarımın gerçek, düzenlenebilir vektör öğelerinden oluşmasını istiyorum.
4. Bir logoyu sadece kabartmak, altına kalın gölge koymak veya renklerini değiştirmek **GNOME'a dönüştürmek değildir**.
5. GNOME gibi göstermek için rastgele televizyon, kamera kasası, hoparlör, kare arka plan, squircle, çerçeve veya madeni para görünümü eklenmesini istemiyorum.
6. Orijinal uygulamanın tanınmasını sağlayan **silüet, karakter/anatomi, poz, negatif boşluk ve ayırt edici renk ilişkileri** bozulmamalı.
7. Kendi kendine tahmin edilmiş, kaynağı olmayan eğriler nedeniyle Firefox'un yüzünün, kuyruğunun veya bir maskotun kollarının bozulmasını istemiyorum.
8. Aynı tasarım reçetesi bütün ikonlara zorlanmamalı. Gerektiğinde düz/geometrik sembol, gerektiğinde maddesel derinlik veya özgün nesne kullanılabilir; karar gerçek referanslarla uyumlu olmalı.
9. **Teknik testlerin geçmesi estetik başarının kanıtı değildir.** Tasarım kötü görünüyorsa "düzeltildi" veya "GNOME oldu" diye sunulmasın.
10. Kaynaklar zaten skill'in içindeyken her simge için sıfırdan aynı internet araştırmasının yapılmasını istemiyorum. Skill'in bilgi ve örnek kütüphanesi kendi kendine yeterli olmalı.
11. Yapılamayan veya doğrulanamayan bir şey varsa başarılı olmuş gibi gösterilmesin; açıkça ifade edilsin.

## 3. Beklediğim GNOME/Adwaita görünümü

Birebir bir GNOME simgesini kopyalamak tek hedefim değil; başka uygulamaların da **GNOME tasarımcıları tarafından yapılmış gibi** birbiriyle tutarlı görünmesini istiyorum.

- **Gerçek GNOME HIG simge tasarımı:** geometrik sadelik, optik denge, karakteristik ve temiz silüet, kontrollü perspektif, amaca uygun malzeme ve gölge.
- **Marka kimliğinin korunması:** Spotify yeşili, Instagram'ın renkleri, Firefox'un tilki/küre geometrisi, TikTok'un nota silüeti gibi uygulamaya özgü öğeler tanınabilir kalmalı.
- **Sahte efektlerden kaçınma:** gereksiz ışık çizgisi, plastik oyuncak görünümü, çok kalın kenarlar, birbiriyle çakışan yüzeyler, gövdeden taşan hatalı katmanlar ve yapay kabartma istemiyorum.
- **Farklı ikon sınıfları:** saf logo/sembol, fiziksel nesne, soyut amblem, oyun görseli, maskot/karakter ve ekran görüntüsünden çıkarılan uygulama kimliği farklı ele alınmalı.
- **Küçük boyutta okunabilirlik:** 32, 48 ve 64 pikselde uygulama tanınmalı; daha büyük önizlemede de ayrıntılar düzgün olmalı.
- **Düzgün arka plan ve saydamlık:** Android ikon paketi için simgenin dışında gereksiz siyah/beyaz ekran görüntüsü zemini bulunmamalı. Özgün biçim uygun olduğunda şeffaf arka plan korunmalı.

**Beğendiğim somut görsel yaklaşım:** Spotify için hazırlanan **“1. Sound Disc”** stili. Sade ana yüzey, kontrollü ince derinlik ve hafif üst ışık vurgusu hoşuma gitti. Instagram'ı da özellikle bu aileye benzer istemiştim. Ancak **bütün simgeleri daireye çevirmek** veya her birine aynı alt çizgiyi eklemek istemiyorum.

## 4. Skill'den beklediğim işleyiş

- Verdiğim görselden uygulamanın asıl ikonunu ayırabilmeli; telefonun durum çubuğunu, galeri arayüzünü ve boş screenshot alanlarını simgeye taşımamalı.
- Uygulamanın ne olduğunu ve onu tanınır kılan öğeleri anlamalı.
- Gerçek **GNOME HIG** ve özgün GNOME SVG'lerini temel almalı; **MoreWaita** ve **Adwaita++** dosyalarını topluluk tarafından oluşturulmuş Adwaita yorumları olarak incelemeli.
- Uygulamanın gerçek SVG'si veya uygun hazırlanmış bir topluluk SVG'si mevcutsa onu açıp katmanlarını ve eğrilerini analiz etmeli. Böyle bir kaynak varsa hatalı şekilleri sıfırdan uydurmamalı.
- Gerektiğinde SVG'yi yeniden tasarlamalı veya düzenlemeli; mevcut bir kaynaktan uyarlama yapılıyorsa bunu gizlememeli.
- Beni her seferinde eski sorunları tekrar anlatmak zorunda bırakmamalı. Önceki reddedilen denemelerden öğrenilmiş kurallar skill'in içinde kalmalı.
- Üretilen tasarımı orijinal görselle ve gerçek GNOME/Adwaita kaynaklarıyla karşılaştırmalı. Hatalı konturlar, üst üste binen parçalar ve kaybolan anatomik ayrıntılar kontrol edilmeli.
- **Düzenlenebilir SVG**, Android'e uygun **şeffaf PNG** (önceki çalışma biçiminde 256×256 ve 512×512) ve **küçük boyut karşılaştırması** teslim edilmeli.
- Bir CandyBar/ikon paketi projesi sağladığımda, üretilen ikonun projeye eklenmesini ve doğru uygulama eşlemesini istiyorum. Gerçek Android paket/aktivite adı doğrulanmadan uydurma eşleme yapılmamalı. Mevcut ikonlar veya XML kayıtları silinmemeli.
- Aynı skill farklı ajanlarda kullanılabilmeli; yalnızca `SKILL.md` değil, referans SVG'leri, lisansları, kod araçları ve örnekleriyle birlikte taşınabilmeli.

## 5. Şimdiye kadarki denemeler ve geri bildirimlerim

| Örnek | İstediğim / sorun |
|---|---|
| Üçgenli medya logosu | Üçgenlerden anlamsız mavi TV/ekran oluşturuldu; özgün kimlik ve GNOME tarzı kayboldu. |
| Instagram | Kalın plastik kamera ve oyuncak görünümlü denemeler hoşuma gitmedi. Sonra Spotify'ın Sound Disc ailesine benzeyen daha sade bir stil istedim. |
| Spotify | **“1. Sound Disc”** tarzını tercih ettim. “Speaker Grille” ile aynı şey değil. |
| Firefox | Kulaklar, yatay burun, mor küre ve yükselen sarı kuyruk bozuldu. Birçok çizim ya yanlış tilkiye dönüştü ya da sadece orijinal logonun gölgeli kopyası oldu. Kaynak SVG'den ilerleyen MoreWaita tabanlı sürüm daha iyi çıktı; sonrasında gövdedeki istenmeyen iç katman/çıkıntıyı özellikle işaretledim. |
| ChatGPT | MoreWaita'daki gerçek düğüm sembolünden iki varyant üretildi (yeşil/teal ve beyaz/ivory). Bu, örnek çalışma; nihai aile kararı verilmedi. |
| TikTok | Nota işaretini ve renk ilişkisinin tanınırlığını korumak önemli; görseldeki küçük şimşek de kaynağın bir öğesi. |
| Clash Royale | Karakter içeren, poster benzeri bir ikon. Sadece sembollere indirgenirse uygulama kimliği kaybolabilir; maskot ve oyun ikonları ayrı ele alınmalı. |
| Beyaz/turkuaz dinozor maskotu | İlk vektör denemesinde kollar birbirine girdi, gövde/ayak anatomisi bozuldu, sırt çıkıntıları kayboldu. Sonraki sürümde özgün konturları korumaya yönelindi. Teknik çıktı, otomatik olarak onaylanmış tasarım değildir. |

Bu geçmiş örnekleri "tasarım zaten tamamlandı" diye değil, **nelerin kabul edilmediğini ve hangi yaklaşımın tercih edildiğini** gösteren kayıtlar olarak görüyorum.

## 6. Eldeki proje dosyaları

Şu kaynakları daha önce yükledim ve bunlar mevcut:

- `HIG-app-icons-master.zip` — GNOME'un orijinal uygulama simgesi tasarım şablonları ve palet dosyaları. Tamamlanmış uygulama simgesi galerisi değil.
- `MoreWaita-main.zip` — MoreWaita'nın gerçek SVG simge kaynakları.
- `adwaita-plus-master.zip` — Adwaita++ simge tema kaynakları.
- `gnome-android-icons-v0.9.zip` — Şu ana kadar hazırlanmış en son skill paketi. **Geliştirilecek başlangıç noktasıdır, kalite onay belgesi değildir.**

Önceki skill sürümlerinde `SKILL.md`, `references/`, gerçek SVG kütüphanesi, örnekler, `scripts/`, karşılaştırma görselleri, testler ve CandyBar yardımcısı bulunuyordu. Son sürümde 54 paketlenmiş gerçek SVG referansı ve daha geniş bir katalog bulunuyor. Bütün katalog kayıtlarının SVG dosyasının paket içinde olduğunu varsaymıyorum.

## 7. Bitmiş sayacağım sonuç

Ben herhangi bir uygulamanın simgesini verdiğimde:

1. Simgenin kimliği ve karakteristik geometrisi korunacak.
2. Sonuç orijinal logo üzerine rastgele efekt eklenmiş gibi değil, **GNOME/Adwaita ikon ailesine aitmiş gibi** görünecek.
3. SVG gerçek vektör olacak; PNG saydam, temiz ve Android ikon paketiyle kullanılabilir olacak.
4. Gerçek GNOME/MoreWaita/Adwaita++ referanslarıyla gözle görülür karşılaştırma yapılmış olacak.
5. Varsa kusurlar gizlenmeyecek; düzeltilmeden başarılı denmeyecek.
6. Projem hazır olduğunda ikonu CandyBar veya seçtiğim eşdeğer yapıya ekleyebileceğim.
7. Bütün bu işlem **görsel üretim aracı kullanmadan** ve skill'in kendi kaynak bilgisinden yararlanarak yapılacak.

## 8. Kaynak bağlantıları — tam liste

### A. GNOME'un resmî kaynakları

- GNOME Human Interface Guidelines: https://developer.gnome.org/hig/
- GNOME HIG — Application Icons: https://developer.gnome.org/hig/guidelines/app-icons
- GNOME HIG — Tools & Resources: https://developer.gnome.org/hig/resources
- GNOME HIG — Color Palette: https://developer.gnome.org/hig/reference/palette.html
- GNOME HIG — UI/Symbolic Icons: https://developer.gnome.org/hig/guidelines/ui-icons.html
- GNOME — Themed Icons: https://developer.gnome.org/documentation/tutorials/themed-icons.html
- GNOME tasarım şablonları (HIG App Icons): https://gitlab.gnome.org/Teams/Design/HIG-app-icons
- Orijinal `template.svg`: https://gitlab.gnome.org/Teams/Design/HIG-app-icons/-/blob/master/template.svg
- GNOME uygulama kataloğu: https://apps.gnome.org/en/
- GNOME Adwaita Icon Theme (resmî GitHub aynası): https://github.com/GNOME/adwaita-icon-theme
- GNOME Adwaita Icon Theme (ana GitLab): https://gitlab.gnome.org/GNOME/adwaita-icon-theme
- GNOME Videos / Totem: https://gitlab.gnome.org/GNOME/totem
- GNOME Videos / Totem GitHub aynası: https://github.com/GNOME/totem
- GNOME Snapshot: https://gitlab.gnome.org/GNOME/snapshot
- GNOME Screenshot: https://gitlab.gnome.org/GNOME/gnome-screenshot
- GNOME Calendar: https://gitlab.gnome.org/GNOME/gnome-calendar
- Tobias Bernard — *Designing an Icon for Your App*: https://blogs.gnome.org/tbernard/2019/12/30/designing-an-icon-for-your-app/
- App Icon Preview (Flathub): https://flathub.org/apps/org.gnome.design.AppIconPreview
- GNOME Snapshot SVG görsel referansı: https://commons.wikimedia.org/wiki/File:GNOME_Snapshot_Icon.svg
- GNOME Totem uygulama simgesi görsel referansı: https://gitlab.gnome.org/uploads/-/system/project/avatar/1855/org.gnome.Totem.png

### B. Topluluk Adwaita kaynakları ve gerçek SVG örnekleri

- MoreWaita: https://github.com/somepaulo/MoreWaita
- MoreWaita Firefox SVG: https://github.com/somepaulo/MoreWaita/blob/main/scalable/apps/firefox.svg
- MoreWaita katkı/tasarım rehberi: https://github.com/somepaulo/MoreWaita/blob/main/CONTRIBUTING.md
- Adwaita++: https://github.com/Bonandry/adwaita-plus

Bu iki tema **resmî GNOME tasarım kılavuzu değil**, topluluk kaynaklarıdır. Orijinal SVG dosyalarının kaynak ve lisanslarıyla birlikte incelenmesini istiyorum.

### C. Android ikon paketi / CandyBar

- CandyBar kütüphanesi: https://github.com/zixpo/candybar
- CandyBar örnek uygulaması: https://github.com/zixpo/candybar-sample
- CandyBar — ikon ekleme ve çalıştırma rehberi: https://github.com/zixpo/candybar-sample/wiki/Adding-icons-and-making-them-work
- Android Adaptive Icons belgeleri (ayrı ikon sistemi): https://developer.android.com/develop/ui/compose/system/icon_design_adaptive

### D. Skill formatı ve çalıştırma ortamları

- Agent Skills Specification: https://agentskills.io/specification
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Codex Skills: https://developers.openai.com/codex/skills
- OpenCode Skills: https://docs.opencode.ai/docs/skills/

### E. Lisans metinleri ve kaynak sahipliği

- GNOME kaynaklarında kullanılan CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- Creative Commons BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/
- GNU GPL lisans bilgileri: https://www.gnu.org/licenses/

**Not:** Yukarıdaki bağlantılar, konuşmamızda ve mevcut skill'in kaynak belgelerinde kullanılan kaynakları kapsar. Yerel ZIP arşivlerindeki tek tek binlerce SVG için ayrıca birer URL dökülmemiştir; bu dosyalar ilgili depoların kendisinde ve yüklediğim arşivlerde bulunuyor.
