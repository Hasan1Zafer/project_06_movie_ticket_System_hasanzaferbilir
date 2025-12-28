"""
Sinema Bilet Rezervasyon Sistemi Ana Program
"""

import os
from datetime import datetime
from movies import (load_movies, save_movies, add_movie, schedule_showtime, 
                   list_showtimes, get_showtime, get_movie, list_active_movies)
from seating import render_seat_map, validate_seat_code
from bookings import (create_booking, cancel_booking, list_customer_bookings, 
                     generate_ticket, get_booking)
from storage import load_state, save_state, backup_state
from reports import (occupancy_report, revenue_summary, top_movies, 
                    peak_days_analysis, showtime_performance_report, export_report)
from validation import (validate_email, validate_phone, validate_date, 
                       validate_time, validate_name, validate_price, validate_duration)


# Klasörler
DATA_DIR = 'data'
BACKUP_DIR = 'backups'
TICKETS_DIR = 'tickets'

# Global değişkenler
movies = []
showtimes = []
seat_maps = {}
bookings = []


def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Devam etmek için bekle"""
    input("\nDevam etmek için Enter'a basın...")


def load_data():
    """Tüm verileri yükle"""
    global movies, showtimes, seat_maps, bookings
    movies = load_movies(os.path.join(DATA_DIR, 'movies.json'))
    showtimes, seat_maps, bookings = load_state(DATA_DIR)
    print("Veriler yüklendi!")


def save_data():
    """Tüm verileri kaydet"""
    save_movies(os.path.join(DATA_DIR, 'movies.json'), movies)
    save_state(DATA_DIR, showtimes, seat_maps, bookings)


def display_header(title):
    """Başlık göster"""
    clear_screen()
    print("=" * 70)
    print(f"{title:^70}")
    print("=" * 70)
    print()


def main_menu():
    """Ana menü"""
    display_header("SİNEMA BİLET SİSTEMİ")
    print("1. Müşteri Menüsü")
    print("2. Admin Menüsü")
    print("3. Raporlar")
    print("4. Yedekleme")
    print("5. Çıkış")
    print()
    return input("Seçiminiz (1-5): ").strip()


def customer_menu():
    """Müşteri menüsü"""
    while True:
        display_header("MÜŞTERİ MENÜSÜ")
        print("1. Filmleri Gör")
        print("2. Seansları Gör")
        print("3. Bilet Al")
        print("4. Rezervasyonlarım")
        print("5. Rezervasyon İptal")
        print("6. Ana Menü")
        print()
        
        choice = input("Seçiminiz (1-6): ").strip()
        
        if choice == '1':
            view_movies()
        elif choice == '2':
            view_showtimes()
        elif choice == '3':
            book_tickets()
        elif choice == '4':
            view_customer_bookings()
        elif choice == '5':
            cancel_booking_menu()
        elif choice == '6':
            break
        else:
            print("Geçersiz seçim!")
            pause()


def admin_menu():
    """Admin menüsü"""
    while True:
        display_header("ADMİN MENÜSÜ")
        print("1. Film Ekle")
        print("2. Seans Planla")
        print("3. Tüm Seanslar")
        print("4. Tüm Rezervasyonlar")
        print("5. Ana Menü")
        print()
        
        choice = input("Seçiminiz (1-5): ").strip()
        
        if choice == '1':
            add_movie_menu()
        elif choice == '2':
            schedule_showtime_menu()
        elif choice == '3':
            view_all_showtimes()
        elif choice == '4':
            view_all_bookings()
        elif choice == '5':
            break
        else:
            print("Geçersiz seçim!")
            pause()


def reports_menu():
    """Raporlar menüsü"""
    while True:
        display_header("RAPORLAR")
        print("1. Doluluk Raporu")
        print("2. Gelir Özeti")
        print("3. En Çok İzlenen Filmler")
        print("4. Yoğun Günler")
        print("5. Seans Performansı")
        print("6. Ana Menü")
        print()
        
        choice = input("Seçiminiz (1-6): ").strip()
        
        if choice == '1':
            show_occupancy_report()
        elif choice == '2':
            show_revenue_summary()
        elif choice == '3':
            show_top_movies()
        elif choice == '4':
            show_peak_days()
        elif choice == '5':
            show_showtime_performance()
        elif choice == '6':
            break
        else:
            print("Geçersiz seçim!")
            pause()


def view_movies():
    """Filmleri göster"""
    display_header("FİLMLER")
    
    active_movies = list_active_movies(movies)
    
    if not active_movies:
        print("Şu anda gösterimde film yok.")
    else:
        for i, movie in enumerate(active_movies, 1):
            print(f"\n{i}. {movie['title']}")
            print(f"   Tür: {movie['genre']}")
            print(f"   Süre: {movie['duration']} dakika")
            print(f"   Puan: {movie['rating']}")
            print(f"   Açıklama: {movie['description']}")
    
    pause()


def view_showtimes():
    """Seansları göster"""
    display_header("SEANSLAR")
    
    if not showtimes:
        print("Henüz planlanmış seans yok.")
        pause()
        return
    
    for i, showtime in enumerate(showtimes, 1):
        movie = get_movie(movies, showtime['movie_id'])
        movie_title = movie['title'] if movie else 'Bilinmeyen'
        
        print(f"\n{i}. {movie_title}")
        print(f"   Tarih: {showtime['date']}")
        print(f"   Saat: {showtime['time']}")
        print(f"   Salon: {showtime['screen']}")
        print(f"   Dil: {showtime['language']}")
        print(f"   Fiyat: Standart ${showtime['pricing']['standard']:.2f}, "
              f"Premium ${showtime['pricing']['premium']:.2f}")
    
    pause()


def book_tickets():
    """Bilet al"""
    display_header("BİLET AL")
    
    if not showtimes:
        print("Henüz planlanmış seans yok.")
        pause()
        return
    
    # Seansları göster
    print("Seanslar:\n")
    for i, showtime in enumerate(showtimes, 1):
        movie = get_movie(movies, showtime['movie_id'])
        movie_title = movie['title'] if movie else 'Bilinmeyen'
        print(f"{i}. {movie_title} - {showtime['date']} {showtime['time']} - {showtime['screen']}")
    
    # Seans seç
    choice = input("\nSeans numarası: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(showtimes)):
        print("Geçersiz seçim!")
        pause()
        return
    
    showtime = showtimes[int(choice) - 1]
    showtime_id = showtime['showtime_id']
    
    # Koltuk haritasını göster
    clear_screen()
    seat_map = seat_maps.get(showtime_id)
    if not seat_map:
        print("Koltuk haritası bulunamadı!")
        pause()
        return
    
    print(render_seat_map(seat_map))
    
    # Koltuk seç
    seats_input = input("Koltuk kodları (virgülle ayırın, örn: A5,A6): ").strip()
    selected_seats = [s.strip().upper() for s in seats_input.split(',')]
    
    # Koltukları kontrol et
    for seat in selected_seats:
        if not validate_seat_code(seat_map, seat):
            print(f"Geçersiz koltuk kodu: {seat}")
            pause()
            return
    
    # Müşteri bilgileri
    print("\nMüşteri Bilgileri:")
    
    # İsim doğrulama
    while True:
        name = input("İsim: ").strip()
        if validate_name(name):
            break
        print("Hata: İsim en az 2 karakter olmalı!")
    
    # Email doğrulama
    while True:
        email = input("E-posta: ").strip()
        if validate_email(email):
            break
        print("Hata: Geçerli bir e-posta adresi girin! (örn: isim@example.com)")
    
    # Telefon doğrulama (opsiyonel)
    while True:
        phone = input("Telefon (opsiyonel, Enter ile geç): ").strip()
        if validate_phone(phone):
            break
        print("Hata: Geçerli bir telefon numarası girin! (10-11 haneli)")
    
    # İndirim seçimi
    print("\nİndirim Seçenekleri:")
    print("1. İndirim yok")
    print("2. Öğrenci indirimi (%10)")
    
    # Grup indirimi otomatik uygulanır
    if len(selected_seats) >= 4:
        print(f"\n🎉 Otomatik Grup İndirimi: 4+ koltuk için %15 indirim uygulanacak!")
        discount_type = 'group'
    else:
        discount_choice = input("\nSeçiminiz (1-2): ").strip()
        discount_type = 'student' if discount_choice == '2' else 'none'
    
    # Fiyat önizlemesi
    pricing = showtime.get('pricing', {'standard': 10.0, 'premium': 15.0})
    seat_map = seat_maps.get(showtime_id)
    from bookings import calculate_booking_total
    preview = calculate_booking_total(selected_seats, pricing, seat_map, discount_type)
    
    print("\n" + "=" * 70)
    print("FİYAT ÖZETİ")
    print("=" * 70)
    print(f"Koltuklar: {', '.join(selected_seats)}")
    print(f"Ara Toplam: ${preview['subtotal']:.2f}")
    if preview['discount'] > 0:
        discount_names = {'student': 'Öğrenci', 'group': 'Grup'}
        print(f"İndirim ({discount_names.get(preview['discount_type'], '')}): -${preview['discount']:.2f}")
    print(f"TOPLAM: ${preview['total']:.2f}")
    print("=" * 70)
    
    confirm = input("\nDevam etmek istiyor musunuz? (evet/hayır): ").strip().lower()
    if confirm != 'evet':
        print("Rezervasyon iptal edildi.")
        pause()
        return
    
    # Rezervasyon oluştur
    try:
        booking_data = {
            'showtime_id': showtime_id,
            'seats': selected_seats,
            'customer_name': name,
            'customer_email': email,
            'customer_phone': phone,
            'discount_type': discount_type
        }
        
        booking = create_booking(showtimes, seat_maps, booking_data)
        bookings.append(booking)
        save_data()
        
        print("\n" + "=" * 70)
        print("REZERVASYON BAŞARILI!")
        print("=" * 70)
        print(f"Rezervasyon ID: {booking['booking_id']}")
        print(f"Koltuklar: {', '.join(booking['seats'])}")
        if booking.get('discount', 0) > 0:
            print(f"Ara Toplam: ${booking.get('subtotal', 0):.2f}")
            print(f"İndirim: -${booking['discount']:.2f}")
        print(f"TOPLAM: ${booking['total']:.2f}")
        print("=" * 70)
        
        # Bilet oluştur
        ticket_path = generate_ticket(booking, TICKETS_DIR)
        if ticket_path:
            print(f"\nBilet kaydedildi: {ticket_path}")
        
    except Exception as e:
        print(f"\nHata: {e}")
    
    pause()


def view_customer_bookings():
    """Müşteri rezervasyonlarını göster"""
    display_header("REZERVASYONLARIM")
    
    email = input("E-posta adresiniz: ").strip()
    
    customer_bookings = list_customer_bookings(bookings, email)
    
    if not customer_bookings:
        print(f"\n{email} için rezervasyon bulunamadı.")
    else:
        for i, booking in enumerate(customer_bookings, 1):
            showtime = get_showtime(showtimes, booking['showtime_id'])
            
            print(f"\n{i}. Rezervasyon ID: {booking['booking_id']}")
            print(f"   Durum: {booking['status']}")
            print(f"   Koltuklar: {', '.join(booking['seats'])}")
            print(f"   Toplam: ${booking['total']:.2f}")
            print(f"   Tarih: {booking['booking_date']}")
            
            if showtime:
                movie = get_movie(movies, showtime['movie_id'])
                movie_title = movie['title'] if movie else 'Bilinmeyen'
                print(f"   Film: {movie_title}")
                print(f"   Seans: {showtime['date']} {showtime['time']}")
    
    pause()


def cancel_booking_menu():
    """Rezervasyon iptali"""
    display_header("REZERVASYON İPTAL")
    
    booking_id = input("Rezervasyon ID: ").strip()
    
    booking = get_booking(bookings, booking_id)
    
    if not booking:
        print("Rezervasyon bulunamadı!")
        pause()
        return
    
    # Rezervasyon detayları
    print(f"\nRezervasyon Detayları:")
    print(f"Rezervasyon ID: {booking['booking_id']}")
    print(f"Müşteri: {booking['customer_name']}")
    print(f"Koltuklar: {', '.join(booking['seats'])}")
    print(f"Toplam: ${booking['total']:.2f}")
    print(f"Durum: {booking['status']}")
    
    confirm = input("\nİptal etmek istediğinizden emin misiniz? (evet/hayır): ").strip().lower()
    
    if confirm == 'evet':
        if cancel_booking(bookings, booking_id, seat_maps):
            save_data()
            print("\nRezervasyon iptal edildi!")
        else:
            print("\nİptal başarısız!")
    else:
        print("\nİptal işlemi durduruldu.")
    
    pause()


def add_movie_menu():
    """Film ekle"""
    display_header("FİLM EKLE")
    
    print("Film bilgilerini girin:\n")
    title = input("Başlık: ").strip()
    genre = input("Tür: ").strip()
    duration = input("Süre (dakika): ").strip()
    rating = input("Puan: ").strip()
    description = input("Açıklama: ").strip()
    
    try:
        duration = int(duration)
        
        movie_data = {
            'title': title,
            'genre': genre,
            'duration': duration,
            'rating': rating,
            'description': description
        }
        
        movie = add_movie(movies, movie_data)
        save_data()
        
        print(f"\nFilm eklendi!")
        print(f"Film ID: {movie['movie_id']}")
        
    except ValueError:
        print("Geçersiz giriş!")
    
    pause()


def schedule_showtime_menu():
    """Seans planla"""
    display_header("SEANS PLANLA")
    
    if not movies:
        print("Önce film eklemelisiniz!")
        pause()
        return
    
    print("Filmler:\n")
    for i, movie in enumerate(movies, 1):
        print(f"{i}. {movie['title']}")
    
    choice = input("\nFilm numarası: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(movies)):
        print("Geçersiz seçim!")
        pause()
        return
    
    movie = movies[int(choice) - 1]
    
    print("\nSeans bilgilerini girin:\n")
    date = input("Tarih (YYYY-MM-DD): ").strip()
    time = input("Saat (HH:MM): ").strip()
    screen = input("Salon (örn: Salon 1): ").strip()
    language = input("Dil: ").strip()
    
    standard_price = input("Standart koltuk fiyatı: $").strip()
    premium_price = input("Premium koltuk fiyatı: $").strip()
    
    try:
        showtime_data = {
            'movie_id': movie['movie_id'],
            'date': date,
            'time': time,
            'screen': screen,
            'language': language,
            'pricing': {
                'standard': float(standard_price),
                'premium': float(premium_price)
            }
        }
        
        showtime = schedule_showtime(showtimes, showtime_data)
        seat_maps[showtime['showtime_id']] = showtime['seat_map']
        save_data()
        
        print(f"\nSeans planlandı!")
        print(f"Seans ID: {showtime['showtime_id']}")
        
    except Exception as e:
        print(f"Hata: {e}")
    
    pause()


def view_all_showtimes():
    """Tüm seansları göster"""
    display_header("TÜM SEANSLAR")
    
    if not showtimes:
        print("Henüz planlanmış seans yok.")
    else:
        for i, showtime in enumerate(showtimes, 1):
            movie = get_movie(movies, showtime['movie_id'])
            movie_title = movie['title'] if movie else 'Bilinmeyen'
            
            print(f"\n{i}. {movie_title}")
            print(f"   Seans ID: {showtime['showtime_id']}")
            print(f"   Tarih: {showtime['date']}")
            print(f"   Saat: {showtime['time']}")
            print(f"   Salon: {showtime['screen']}")
            print(f"   Dil: {showtime['language']}")
    
    pause()


def view_all_bookings():
    """Tüm rezervasyonları göster"""
    display_header("TÜM REZERVASYONLAR")
    
    if not bookings:
        print("Henüz rezervasyon yok.")
    else:
        active_count = len([b for b in bookings if b['status'] != 'cancelled'])
        cancelled_count = len([b for b in bookings if b['status'] == 'cancelled'])
        
        print(f"Toplam Rezervasyon: {len(bookings)}")
        print(f"Aktif: {active_count}")
        print(f"İptal Edilmiş: {cancelled_count}\n")
        
        for i, booking in enumerate(bookings[:20], 1):
            print(f"{i}. {booking['booking_id'][:8]} - {booking['customer_name']} - "
                  f"${booking['total']:.2f} - {booking['status']}")
    
    pause()


def show_occupancy_report():
    """Doluluk raporu"""
    display_header("DOLULUK RAPORU")
    
    report = occupancy_report(showtimes, seat_maps, bookings)
    
    print("Genel Doluluk:")
    print(f"Toplam Koltuk: {report['overall']['total_seats']}")
    print(f"Dolu Koltuk: {report['overall']['sold_seats']}")
    print(f"Doluluk Oranı: %{report['overall']['occupancy_rate']}")
    
    print("\n" + "=" * 70)
    print("Seanslar:")
    print("=" * 70)
    
    for st_report in report['showtimes'][:10]:
        movie = get_movie(movies, st_report['movie_id'])
        movie_title = movie['title'] if movie else 'Bilinmeyen'
        
        print(f"\n{movie_title} - {st_report['date']} {st_report['time']}")
        print(f"  Kapasite: {st_report['capacity']}")
        print(f"  Dolu: {st_report['sold']}")
        print(f"  Doluluk: %{st_report['occupancy_rate']}")
    
    export = input("\nDosyaya kaydet? (evet/hayır): ").strip().lower()
    if export == 'evet':
        filename = f"doluluk_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = export_report(report, filename)
        print(f"Rapor kaydedildi: {filepath}")
    
    pause()


def show_revenue_summary():
    """Gelir özeti"""
    display_header("GELİR ÖZETİ")
    
    print("Zaman aralığı girin:")
    start_date = input("Başlangıç tarihi (YYYY-MM-DD): ").strip()
    end_date = input("Bitiş tarihi (YYYY-MM-DD): ").strip()
    
    summary = revenue_summary(bookings, (start_date, end_date))
    
    print("\n" + "=" * 70)
    print(f"Dönem: {summary['period']['start']} - {summary['period']['end']}")
    print("=" * 70)
    print(f"Toplam Gelir: ${summary['total_revenue']:.2f}")
    print(f"Toplam Rezervasyon: {summary['total_bookings']}")
    print(f"Toplam Bilet: {summary['total_tickets']}")
    print(f"Ortalama Bilet Fiyatı: ${summary['average_ticket_price']:.2f}")
    
    pause()


def show_top_movies():
    """En çok izlenen filmler"""
    display_header("EN ÇOK İZLENEN FİLMLER")
    
    limit = input("Kaç film gösterilsin? (varsayılan 5): ").strip()
    limit = int(limit) if limit.isdigit() else 5
    
    top = top_movies(bookings, showtimes, limit)
    
    if not top:
        print("Henüz veri yok.")
    else:
        print(f"\nEn Çok Gelir Getiren {limit} Film:\n")
        for i, movie_stat in enumerate(top, 1):
            movie = get_movie(movies, movie_stat['movie_id'])
            movie_title = movie['title'] if movie else 'Bilinmeyen'
            
            print(f"{i}. {movie_title}")
            print(f"   Gelir: ${movie_stat['revenue']:.2f}")
            print(f"   Satılan Bilet: {movie_stat['tickets_sold']}")
            print(f"   Rezervasyon: {movie_stat['bookings']}\n")
    
    pause()


def show_peak_days():
    """Yoğun günler"""
    display_header("YOĞUN GÜNLER")
    
    analysis = peak_days_analysis(bookings)
    
    print(f"Toplam Aktif Gün: {analysis['total_days']}\n")
    print("En Yoğun 10 Gün:\n")
    
    for i, day in enumerate(analysis['peak_days'], 1):
        print(f"{i}. {day['date']}")
        print(f"   Rezervasyon: {day['bookings']}")
        print(f"   Bilet: {day['tickets']}")
        print(f"   Gelir: ${day['revenue']:.2f}\n")
    
    pause()


def show_showtime_performance():
    """Seans performansı"""
    display_header("SEANS PERFORMANSI")
    
    if not showtimes:
        print("Henüz planlanmış seans yok.")
        pause()
        return
    
    print("Seanslar:\n")
    for i, showtime in enumerate(showtimes, 1):
        movie = get_movie(movies, showtime['movie_id'])
        movie_title = movie['title'] if movie else 'Bilinmeyen'
        print(f"{i}. {movie_title} - {showtime['date']} {showtime['time']}")
    
    choice = input("\nSeans numarası: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(showtimes)):
        print("Geçersiz seçim!")
        pause()
        return
    
    showtime = showtimes[int(choice) - 1]
    
    performance = showtime_performance_report(showtimes, seat_maps, bookings, showtime['showtime_id'])
    
    if 'error' in performance:
        print(f"\nHata: {performance['error']}")
    else:
        movie = get_movie(movies, performance['movie_id'])
        movie_title = movie['title'] if movie else 'Bilinmeyen'
        
        print("\n" + "=" * 70)
        print(f"{movie_title} - {performance['date']} {performance['time']}")
        print("=" * 70)
        print(f"Salon: {performance['screen']}")
        print(f"Kapasite: {performance['capacity']}")
        print(f"Satılan Koltuk: {performance['seats_sold']}")
        print(f"Doluluk Oranı: %{performance['occupancy_rate']}")
        print(f"Toplam Rezervasyon: {performance['total_bookings']}")
        print(f"Toplam Gelir: ${performance['total_revenue']:.2f}")
        print(f"Ortalama Rezervasyon Değeri: ${performance['average_booking_value']:.2f}")
    
    pause()


def backup_data_menu():
    """Veri yedekleme"""
    display_header("VERİ YEDEKLEME")
    
    backup_files = backup_state(DATA_DIR, BACKUP_DIR)
    
    if backup_files:
        print("Yedekleme başarılı!")
        print(f"\n{len(backup_files)} dosya yedeklendi:")
        for filepath in backup_files:
            print(f"  - {filepath}")
    else:
        print("Yedekleme başarısız!")
    
    pause()


def initialize_sample_data():
    """Örnek veri oluştur"""
    global movies, showtimes, seat_maps, bookings
    
    # Klasörleri oluştur
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(TICKETS_DIR, exist_ok=True)
    
    movies_path = os.path.join(DATA_DIR, 'movies.json')
    
    if not os.path.exists(movies_path) or os.path.getsize(movies_path) == 0:
        # Örnek filmler
        sample_movies = [
            {
                'title': 'Matrix',
                'genre': 'Bilim Kurgu',
                'duration': 136,
                'rating': 'R',
                'description': 'Gerçekliğin doğasını keşfeden bir hacker.'
            },
            {
                'title': 'Inception',
                'genre': 'Gerilim',
                'duration': 148,
                'rating': 'PG-13',
                'description': 'Rüya paylaşımı ile şirket sırlarını çalan bir hırsız.'
            }
        ]
        
        for movie_data in sample_movies:
            add_movie(movies, movie_data)
        
        # Örnek seanslar
        for movie in movies:
            showtime_data = {
                'movie_id': movie['movie_id'],
                'date': '2025-01-15',
                'time': '14:00',
                'screen': 'Salon 1',
                'language': 'Türkçe',
                'pricing': {
                    'standard': 12.0,
                    'premium': 18.0
                }
            }
            showtime = schedule_showtime(showtimes, showtime_data)
            seat_maps[showtime['showtime_id']] = showtime['seat_map']
        
        save_data()
        print("Örnek veriler oluşturuldu!")


def main():
    """Ana program"""
    print("Sinema Bilet Sistemi yükleniyor...")
    
    # Örnek veri oluştur
    initialize_sample_data()
    
    # Verileri yükle
    load_data()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            customer_menu()
        elif choice == '2':
            admin_menu()
        elif choice == '3':
            reports_menu()
        elif choice == '4':
            backup_data_menu()
        elif choice == '5':
            print("\nSistemden çıkılıyor...")
            save_data()
            break
        else:
            print("Geçersiz seçim!")
            pause()


if __name__ == "__main__":
    main()
