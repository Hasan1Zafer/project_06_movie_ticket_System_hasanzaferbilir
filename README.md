# project_06_movie_ticket_System_hasanzaferbilir

## 📋 Proje Özellikleri

### 1. Rezervasyon ve Koltuk Yönetimi 
- ✅ Film seansı oluşturma ve yönetimi
- ✅ 8x12 koltuk haritası (Premium: A-B sıraları, Standart: C-H sıraları)
- ✅ Gerçek zamanlı koltuk müsaitlik kontrolü
- ✅ Çoklu koltuk rezervasyonu
- ✅ Rezervasyon iptali ve koltuk serbest bırakma

### 2. Veri Saklama ve Kurtarma 
- ✅ JSON dosya tabanlı veri saklama
- ✅ Film, seans, rezervasyon verilerinin kalıcı tutulması
- ✅ Yedekleme sistemi (backups/ klasörü)
- ✅ Otomatik veri yükleme/kaydetme

### 3. Fiyatlandırma ve İndirim Sistemi 
- ✅ Premium/Standart koltuk fiyatlandırması
- ✅ Öğrenci indirimi (%10)
- ✅ Grup indirimi (4+ koltuk için %15)
- ✅ Otomatik fiyat hesaplama

### 4. Raporlama ve Analitik 
- ✅ Doluluk oranı raporu
- ✅ Gelir özeti (tarih aralığına göre)
- ✅ En çok izlenen filmler
- ✅ Yoğun günler analizi
- ✅ Seans performans raporu

### 5. Veri Doğrulama ve Güvenilirlik 
- ✅ Email format kontrolü
- ✅ Koltuk kodu validasyonu
- ✅ Çift rezervasyon engelleme
- ✅ Tarih format kontrolü

### 6. Dokümantasyon ve Kullanıcı Deneyimi 
- ✅ Türkçe menüler ve mesajlar
- ✅ Detaylı kullanım kılavuzu 
- ✅ Kod içi yorumlar
- ✅ Basit ve anlaşılır arayüz

### 7. Test ve Kod Kalitesi 
- ✅ 12+ otomatik test
- ✅ Test kapsamı: Koltuk, Rezervasyon, Film yönetimi
- ✅ Tüm testler başarılı
- ✅ Temiz ve okunabilir kod

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Standart Python kütüphaneleri (harici bağımlılık yok)

### Adımlar

1. **Projeyi indirin**
```bash
cd project_06_movie_ticket_System_hasanzaferbilir
```

2. **Sanal ortam oluşturun**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# veya
.venv\Scripts\activate  # Windows
```

3. **Programı çalıştırın**
```bash
python main.py
```

## 📖 Kullanım Kılavuzu

### Sistem İlk Çalıştırma
Program ilk çalıştırıldığında otomatik olarak:
- `data/` klasörü ve örnek filmler oluşturur
- İki örnek seans planlar (Matrix ve Inception)
- Boş koltuk haritaları hazırlar

### 1. Müşteri İşlemleri

#### Bilet Alma (Tam Akış)
1. Ana menüden **"1. Müşteri Menüsü"** seçin
2. **"3. Bilet Al"** seçeneğine tıklayın
3. Gösterilen seanslardan birini seçin
4. Koltuk haritasında müsait koltukları görün
5. Koltuk kodlarını girin (örn: `A5,A6` - virgülle ayırarak)
6. Müşteri bilgilerini girin:
   - İsim
   - E-posta
   - Telefon (opsiyonel)
7. İndirim seçimi yapın:
   - Öğrenci indirimi (%10)
   - Grup indirimi (4+ koltuk otomatik %15)
8. Onay ekranında toplam tutarı görün
9. Rezervasyon ID'nizi ve biletinizi alın

**Örnek:**
```
Koltuk kodları: A5,A6,A7
Müşteri: Ahmet Yılmaz
E-posta: ahmet@example.com
İndirim: Öğrenci (%10)

Toplam: 3 premium koltuk × $18.00 = $54.00
İndirim: -$5.40
Ödenecek: $48.60
```

#### Rezervasyonlarımı Görüntüleme
1. **"4. Rezervasyonlarım"** seçin
2. E-posta adresinizi girin
3. Tüm rezervasyonlarınızı görün

#### Rezervasyon İptali
1. **"5. Rezervasyon İptal"** seçin
2. Rezervasyon ID'nizi girin
3. Onaylayın
4. Koltuklar otomatik serbest bırakılır

### 2. Admin İşlemleri

#### Yeni Film Ekleme
1. Ana menüden **"2. Admin Menüsü"** seçin
2. **"1. Film Ekle"** seçin
3. Film bilgilerini girin:
   - Başlık
   - Tür (Aksiyon, Dram, Komedi vb.)
   - Süre (dakika)
   - Puan (PG, PG-13, R vb.)
   - Açıklama

#### Seans Planlama
1. **"2. Seans Planla"** seçin
2. Film seçin
3. Seans bilgilerini girin:
   - Tarih (YYYY-MM-DD formatında)
   - Saat (HH:MM formatında)
   - Salon (örn: Salon 1)
   - Dil (Türkçe, İngilizce, Altyazılı vb.)
   - Standart koltuk fiyatı
   - Premium koltuk fiyatı

### 3. Raporlar

#### Doluluk Raporu
- Tüm seansların doluluk oranlarını gösterir
- Toplam kapasite ve satılan koltukları listeler
- JSON formatında dışa aktarma seçeneği

#### Gelir Özeti
- Belirli tarih aralığında toplam geliri gösterir
- Satılan bilet sayısı
- Ortalama bilet fiyatı
- Toplam rezervasyon sayısı

#### En Çok İzlenen Filmler
- Gelire göre en çok kazandıran filmleri sıralar
- Her film için:
  - Toplam gelir
  - Satılan bilet sayısı
  - Rezervasyon sayısı

## 🧪 Testleri Çalıştırma

```bash
python test_system.py
```

**Test Kapsamı:**
- Koltuk haritası oluşturma
- Koltuk rezervasyonu ve iptali
- Çift rezervasyon engelleme
- Premium/Standart fiyatlandırma
- Rezervasyon oluşturma
- İndirim hesaplama
- Film ve seans yönetimi

**Beklenen Sonuç:**
```
Ran 12 tests in 0.001s
OK
Başarılı: 12
Başarısız: 0
```

## 📁 Proje Yapısı

```
project_06_movie_ticket_System_hasanzaferbilir/
├── main.py              # Ana program ve menüler
├── movies.py            # Film ve seans yönetimi
├── seating.py           # Koltuk haritası yönetimi
├── bookings.py          # Rezervasyon işlemleri
├── reports.py           # Raporlama ve analitik
├── storage.py           # Veri saklama/yükleme
├── test_system.py       # Otomatik testler
├── requirements.txt     # Python bağımlılıkları
├── data/               # Veri dosyaları
│   ├── movies.json
│   ├── showtimes.json
│   └── bookings.json
├── backups/            # Yedek dosyaları
└── tickets/            # Oluşturulan biletler
```

## 💾 Veri Yedekleme

Sistem otomatik veri kaydeder, ancak manuel yedek almak için:
1. Ana menüden **"4. Yedekleme"** seçin
2. Timestamp'li yedek dosyaları `backups/` klasörüne kaydedilir
3. Yedek dosyaları:
   - `movies_YYYYMMDD_HHMMSS.json`
   - `showtimes_YYYYMMDD_HHMMSS.json`
   - `bookings_YYYYMMDD_HHMMSS.json`

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: Grup Bilet Alımı
```
1. Müşteri Menüsü → Bilet Al
2. Matrix seansını seç
3. 5 koltuk seç: A1,A2,A3,A4,A5
4. Müşteri bilgilerini gir
5. Grup indirimi otomatik uygulanır (%15)
6. Rezervasyon tamamlanır
```

### Senaryo 2: Öğrenci Bilet Alımı
```
1. Müşteri Menüsü → Bilet Al
2. Inception seansını seç
3. 2 koltuk seç: C5,C6
4. Müşteri bilgilerini gir
5. Öğrenci indirimi seç (%10)
6. İndirimli fiyat hesaplanır
7. Rezervasyon tamamlanır
```

### Senaryo 3: Rezervasyon İptali
```
1. Müşteri Menüsü → Rezervasyon İptal
2. Rezervasyon ID: abc123...
3. Rezervasyon detaylarını kontrol et
4. İptal et → "evet"
5. Koltuklar serbest bırakılır
6. Başkaları o koltukları alabilir
```

## 🔧 Sorun Giderme

### Program başlamıyor
- Python 3.8+ kurulu olduğundan emin olun
- Sanal ortamı aktifleştirin
- `python --version` ile kontrol edin

### Veriler kayboldu
- `backups/` klasöründeki yedeklere bakın
- JSON dosyalarını `data/` klasörüne kopyalayın

### Test başarısız
- Tüm Python dosyalarının güncel olduğundan emin olun
- `data/` klasörünü temizleyip yeniden başlatın




## 👨‍💻 Developed

Hasan Zafer Bilir

---


