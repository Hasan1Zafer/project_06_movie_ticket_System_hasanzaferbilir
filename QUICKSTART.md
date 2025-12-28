# 🚀 Hızlı Başlangıç Kılavuzu

## 5 Dakikada Başlayın!

### 1. Kurulum (2 dakika)

```bash
# Sanal ortam oluştur
python -m venv .venv

# Aktifleştir
source .venv/bin/activate  # macOS/Linux

# Programı çalıştır
python main.py
```

### 2. İlk Rezervasyonunuz (3 dakika)

#### Adım 1: Ana Menü
```
===========================================
         SİNEMA BİLET SİSTEMİ
===========================================

1. Müşteri Menüsü
2. Admin Menüsü
3. Raporlar
4. Yedekleme
5. Çıkış

Seçiminiz (1-5): 1
```

#### Adım 2: Bilet Al
```
1. Filmleri Gör
2. Seansları Gör
3. Bilet Al  ← BURAYA
4. Rezervasyonlarım
5. Rezervasyon İptal
6. Ana Menü

Seçiminiz (1-6): 3
```

#### Adım 3: Seans Seç
```
Seanslar:

1. Matrix - 2025-01-15 14:00 - Salon 1
2. Inception - 2025-01-15 14:00 - Salon 1

Seans numarası: 1  ← Matrix'i seçtik
```

#### Adım 4: Koltuk Seç
```
============================================================
                         PERDE
============================================================
Açıklama: [M] Müsait  [D] Dolu

      1   2   3   4   5   6   7   8   9  10  11  12
A  [M] [M] [M] [M] [M] [M] [M] [M] [M] [M] [M] [M]  (PREMIUM)
B  [M] [M] [M] [M] [M] [M] [M] [M] [M] [M] [M] [M]  (PREMIUM)
C  [M] [M] [M] [M] [M] [M] [M] [M] [M] [M] [M] [M]  (STANDART)
...

Koltuk kodları: A5,A6  ← 2 premium koltuk seçtik
```

#### Adım 5: Müşteri Bilgileri
```
Müşteri Bilgileri:
İsim: Ahmet Yılmaz
E-posta: ahmet@example.com
Telefon: 5551234567

İndirim Seçenekleri:
1. İndirim yok
2. Öğrenci indirimi (%10)

Seçiminiz (1-2): 2  ← Öğrenci indirimi seçtik
```

#### Adım 6: Onay ve Sonuç
```
======================================================================
FİYAT ÖZETİ
======================================================================
Koltuklar: A5, A6
Ara Toplam: $36.00
İndirim (Öğrenci): -$3.60
TOPLAM: $32.40
======================================================================

Devam etmek istiyor musunuz? (evet/hayır): evet

======================================================================
REZERVASYON BAŞARILI!
======================================================================
Rezervasyon ID: abc123-def456-789...
Koltuklar: A5, A6
Ara Toplam: $36.00
İndirim: -$3.60
TOPLAM: $32.40
======================================================================

Bilet kaydedildi: tickets/ticket_abc123.txt
```

### 3. Rezervasyonu Görüntüleme

```
Müşteri Menüsü → 4. Rezervasyonlarım

E-posta adresiniz: ahmet@example.com

1. Rezervasyon ID: abc123-def456-789...
   Durum: confirmed
   Koltuklar: A5, A6
   Toplam: $32.40
   Tarih: 2025-12-29 14:30:00
   Film: Matrix
   Seans: 2025-01-15 14:00
```

### 4. Rezervasyon İptali

```
Müşteri Menüsü → 5. Rezervasyon İptal

Rezervasyon ID: abc123-def456-789...

Rezervasyon Detayları:
Müşteri: Ahmet Yılmaz
Koltuklar: A5, A6
Toplam: $32.40
Durum: confirmed

İptal etmek istediğinizden emin misiniz? (evet/hayır): evet

Rezervasyon iptal edildi!
```

## 🎯 Önemli Özellikler

### İndirimler
- **Öğrenci İndirimi:** %10 indirim
- **Grup İndirimi:** 4+ koltuk için otomatik %15 indirim

### Koltuk Tipleri
- **Premium (A-B):** $18.00
- **Standart (C-H):** $12.00

### Örnek Fiyatlar
```
2 Premium koltuk (öğrenci): $36 - $3.60 = $32.40
5 Standart koltuk (grup): $60 - $9.00 = $51.00
1 Premium + 1 Standart: $18 + $12 = $30.00
```

## 🧪 Testleri Çalıştırma

```bash
python test_system.py
```

**Beklenen:** 24 test başarılı ✅

## 💡 İpuçları

1. **Email formatı:** user@domain.com şeklinde olmalı
2. **Telefon:** 10-11 haneli numara veya boş bırakın
3. **Koltuk seçimi:** Virgülle ayırın (örn: A5,A6,B3)
4. **4+ koltuk:** Otomatik grup indirimi alırsınız!
5. **Rezervasyon ID:** Saklamanız önemli (iptal için gerekli)

## 🆘 Sorun mu var?

```bash
# Testleri çalıştır
python test_system.py

# Verileri sıfırla
rm -rf data/
python main.py  # Otomatik örnek veri oluşturur
```

## 📚 Detaylı Bilgi

README.md dosyasına bakın - tam dokümantasyon!

---

**Hazır mısınız? Haydi başlayalım! 🎬**

```bash
python main.py
```
