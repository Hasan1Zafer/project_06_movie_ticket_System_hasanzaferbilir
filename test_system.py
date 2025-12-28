"""
Sinema Bilet Sistemi Test Dosyası
"""

import unittest
import os
from movies import add_movie, schedule_showtime, list_showtimes
from seating import initialize_seat_map, is_seat_available, reserve_seat, release_seat, get_seat_zone
from bookings import create_booking, cancel_booking, calculate_booking_total
from validation import validate_email, validate_phone, validate_date, validate_time, validate_name


class TestSeating(unittest.TestCase):
    """Koltuk yönetimi testleri"""
    
    def setUp(self):
        """Test için koltuk haritası oluştur"""
        self.seat_map = initialize_seat_map()
    
    def test_seat_map_initialization(self):
        """Koltuk haritası doğru oluşturuldu mu"""
        # 8 sıra x 12 koltuk = 96 koltuk olmalı
        self.assertEqual(len(self.seat_map['seats']), 96)
        
        # Tüm koltuklar başlangıçta müsait olmalı
        for seat_code, seat_info in self.seat_map['seats'].items():
            self.assertEqual(seat_info['status'], 'available')
    
    def test_seat_availability(self):
        """Koltuk müsaitlik kontrolü"""
        # Başlangıçta müsait olmalı
        self.assertTrue(is_seat_available(self.seat_map, 'A5'))
        
        # Rezerve et
        reserve_seat(self.seat_map, 'A5')
        
        # Artık müsait olmamalı
        self.assertFalse(is_seat_available(self.seat_map, 'A5'))
    
    def test_seat_reservation(self):
        """Koltuk rezervasyonu"""
        # Bir koltuğu rezerve et
        seat_info = reserve_seat(self.seat_map, 'C3')
        
        # Koltuk dolu olarak işaretlenmeli
        self.assertEqual(seat_info['status'], 'sold')
        self.assertEqual(self.seat_map['seats']['C3']['status'], 'sold')
    
    def test_double_booking_prevention(self):
        """Çift rezervasyon engellenmeli"""
        # Koltuğu rezerve et
        reserve_seat(self.seat_map, 'D7')
        
        # Aynı koltuğu tekrar rezerve etmeye çalış - hata vermeli
        with self.assertRaises(ValueError):
            reserve_seat(self.seat_map, 'D7')
    
    def test_seat_release(self):
        """Koltuk serbest bırakma"""
        # Rezerve edip sonra serbest bırak
        reserve_seat(self.seat_map, 'E10')
        seat_info = release_seat(self.seat_map, 'E10')
        
        # Koltuk tekrar müsait olmalı
        self.assertEqual(seat_info['status'], 'available')
        self.assertTrue(is_seat_available(self.seat_map, 'E10'))
    
    def test_seat_zones(self):
        """Premium ve standart koltuk bölgeleri"""
        # A ve B sıraları premium olmalı
        self.assertEqual(get_seat_zone(self.seat_map, 'A5'), 'premium')
        self.assertEqual(get_seat_zone(self.seat_map, 'B8'), 'premium')
        
        # Diğer sıralar standart olmalı
        self.assertEqual(get_seat_zone(self.seat_map, 'C5'), 'standard')
        self.assertEqual(get_seat_zone(self.seat_map, 'H12'), 'standard')


class TestBookings(unittest.TestCase):
    """Rezervasyon testleri"""
    
    def setUp(self):
        """Test verisi oluştur"""
        self.movies = []
        self.showtimes = []
        self.seat_maps = {}
        self.bookings = []
        
        # Test filmi ekle
        movie_data = {
            'title': 'Test Film',
            'genre': 'Aksiyon',
            'duration': 120,
            'rating': 'PG-13',
            'description': 'Test açıklaması'
        }
        self.movie = add_movie(self.movies, movie_data)
        
        # Test seansı planla
        showtime_data = {
            'movie_id': self.movie['movie_id'],
            'date': '2025-01-20',
            'time': '18:00',
            'screen': 'Salon 1',
            'language': 'Türkçe',
            'pricing': {
                'standard': 10.0,
                'premium': 15.0
            }
        }
        self.showtime = schedule_showtime(self.showtimes, showtime_data)
        self.seat_maps[self.showtime['showtime_id']] = self.showtime['seat_map']
    
    def test_booking_creation(self):
        """Rezervasyon oluşturma"""
        booking_data = {
            'showtime_id': self.showtime['showtime_id'],
            'seats': ['C5', 'C6'],
            'customer_name': 'Ali Yılmaz',
            'customer_email': 'ali@test.com'
        }
        
        booking = create_booking(self.showtimes, self.seat_maps, booking_data)
        
        # Rezervasyon oluşturuldu mu
        self.assertIn('booking_id', booking)
        self.assertEqual(booking['seats'], ['C5', 'C6'])
        self.assertEqual(booking['customer_email'], 'ali@test.com')
        self.assertEqual(booking['status'], 'confirmed')
    
    def test_booking_total_calculation(self):
        """Toplam fiyat hesaplama"""
        seat_map = initialize_seat_map()
        
        pricing = {'standard': 10.0, 'premium': 15.0}
        seats = ['A5', 'A6', 'C3']  # 2 premium, 1 standart
        
        result = calculate_booking_total(seats, pricing, seat_map, 'none')
        
        # Beklenen: 2*15 + 1*10 = 40
        self.assertEqual(result['total'], 40.0)
        self.assertEqual(result['discount'], 0.0)
    
    def test_student_discount(self):
        """Öğrenci indirimi testi (%10)"""
        seat_map = initialize_seat_map()
        
        pricing = {'standard': 10.0, 'premium': 15.0}
        seats = ['A5', 'A6']  # 2 premium = $30
        
        result = calculate_booking_total(seats, pricing, seat_map, 'student')
        
        # Beklenen: 30 - 3 (10% indirim) = 27
        self.assertEqual(result['subtotal'], 30.0)
        self.assertEqual(result['discount'], 3.0)
        self.assertEqual(result['total'], 27.0)
        self.assertEqual(result['discount_type'], 'student')
    
    def test_group_discount(self):
        """Grup indirimi testi (%15 - 4+ koltuk)"""
        seat_map = initialize_seat_map()
        
        pricing = {'standard': 10.0, 'premium': 15.0}
        seats = ['C1', 'C2', 'C3', 'C4']  # 4 standart = $40
        
        result = calculate_booking_total(seats, pricing, seat_map, 'none')
        
        # 4+ koltuk olduğu için otomatik grup indirimi uygulanmalı
        # Beklenen: 40 - 6 (15% indirim) = 34
        self.assertEqual(result['subtotal'], 40.0)
        self.assertEqual(result['discount'], 6.0)
        self.assertEqual(result['total'], 34.0)
        self.assertEqual(result['discount_type'], 'group')
    
    def test_booking_cancellation(self):
        """Rezervasyon iptali"""
        # Rezervasyon oluştur
        booking_data = {
            'showtime_id': self.showtime['showtime_id'],
            'seats': ['D5', 'D6'],
            'customer_name': 'Ayşe Demir',
            'customer_email': 'ayse@test.com'
        }
        
        booking = create_booking(self.showtimes, self.seat_maps, booking_data)
        self.bookings.append(booking)
        
        # Rezervasyonu iptal et
        result = cancel_booking(self.bookings, booking['booking_id'], self.seat_maps)
        
        # İptal başarılı mı
        self.assertTrue(result)
        self.assertEqual(booking['status'], 'cancelled')
        
        # Koltuklar serbest bırakıldı mı
        self.assertTrue(is_seat_available(
            self.seat_maps[self.showtime['showtime_id']], 'D5'
        ))


class TestMovies(unittest.TestCase):
    """Film yönetimi testleri"""
    
    def test_add_movie(self):
        """Film ekleme"""
        movies = []
        movie_data = {
            'title': 'Test Filmi',
            'genre': 'Dram',
            'duration': 150,
            'rating': 'R',
            'description': 'Bir test filmi'
        }
        
        movie = add_movie(movies, movie_data)
        
        self.assertEqual(len(movies), 1)
        self.assertEqual(movie['title'], 'Test Filmi')
        self.assertIn('movie_id', movie)
    
    def test_schedule_showtime(self):
        """Seans planlama"""
        movies = []
        showtimes = []
        
        movie = add_movie(movies, {
            'title': 'Test',
            'genre': 'Aksiyon',
            'duration': 120,
            'rating': 'PG-13',
            'description': 'Test'
        })
        
        showtime_data = {
            'movie_id': movie['movie_id'],
            'date': '2025-01-25',
            'time': '20:00',
            'screen': 'Salon 2',
            'language': 'Türkçe',
            'pricing': {'standard': 12.0, 'premium': 18.0}
        }
        
        showtime = schedule_showtime(showtimes, showtime_data)
        
        self.assertEqual(len(showtimes), 1)
        self.assertIn('showtime_id', showtime)
        self.assertIn('seat_map', showtime)
    
    def test_list_showtimes_filter(self):
        """Seans filtreleme"""
        movies = []
        showtimes = []
        
        # İki film ekle
        movie1 = add_movie(movies, {
            'title': 'Film 1',
            'genre': 'Aksiyon',
            'duration': 120,
            'rating': 'PG-13',
            'description': 'Test'
        })
        
        movie2 = add_movie(movies, {
            'title': 'Film 2',
            'genre': 'Komedi',
            'duration': 90,
            'rating': 'PG',
            'description': 'Test'
        })
        
        # Seanslar planla
        schedule_showtime(showtimes, {
            'movie_id': movie1['movie_id'],
            'date': '2025-01-25',
            'time': '14:00',
            'pricing': {'standard': 10.0, 'premium': 15.0}
        })
        
        schedule_showtime(showtimes, {
            'movie_id': movie2['movie_id'],
            'date': '2025-01-25',
            'time': '16:00',
            'pricing': {'standard': 10.0, 'premium': 15.0}
        })
        
        # Filme göre filtrele
        filtered = list_showtimes(showtimes, movie_id=movie1['movie_id'])
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['movie_id'], movie1['movie_id'])


class TestValidation(unittest.TestCase):
    """Veri doğrulama testleri"""
    
    def test_valid_email(self):
        """Geçerli email adresleri"""
        self.assertTrue(validate_email('test@example.com'))
        self.assertTrue(validate_email('user.name@domain.co.uk'))
        self.assertTrue(validate_email('ahmet123@test.com'))
    
    def test_invalid_email(self):
        """Geçersiz email adresleri"""
        self.assertFalse(validate_email('invalid'))
        self.assertFalse(validate_email('test@'))
        self.assertFalse(validate_email('@example.com'))
        self.assertFalse(validate_email('test @example.com'))
    
    def test_valid_phone(self):
        """Geçerli telefon numaraları"""
        self.assertTrue(validate_phone('5551234567'))
        self.assertTrue(validate_phone('05551234567'))
        self.assertTrue(validate_phone(''))  # Opsiyonel
    
    def test_invalid_phone(self):
        """Geçersiz telefon numaraları"""
        self.assertFalse(validate_phone('123'))
        self.assertFalse(validate_phone('abcdefghij'))
    
    def test_valid_date(self):
        """Geçerli tarih formatları"""
        self.assertTrue(validate_date('2025-01-20'))
        self.assertTrue(validate_date('2024-12-31'))
    
    def test_invalid_date(self):
        """Geçersiz tarih formatları"""
        self.assertFalse(validate_date('2025/01/20'))
        self.assertFalse(validate_date('20-01-2025'))
        self.assertFalse(validate_date('invalid'))
    
    def test_valid_time(self):
        """Geçerli saat formatları"""
        self.assertTrue(validate_time('14:30'))
        self.assertTrue(validate_time('09:00'))
    
    def test_invalid_time(self):
        """Geçersiz saat formatları"""
        self.assertFalse(validate_time('14:30:00'))
        self.assertFalse(validate_time('25:00'))
        self.assertFalse(validate_time('invalid'))
    
    def test_valid_name(self):
        """Geçerli isimler"""
        self.assertTrue(validate_name('Ahmet'))
        self.assertTrue(validate_name('Ali Yılmaz'))
    
    def test_invalid_name(self):
        """Geçersiz isimler"""
        self.assertFalse(validate_name('A'))
        self.assertFalse(validate_name(''))
        self.assertFalse(validate_name('  '))


def run_tests():
    """Tüm testleri çalıştır"""
    # Test paketi oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestSeating))
    suite.addTests(loader.loadTestsFromTestCase(TestBookings))
    suite.addTests(loader.loadTestsFromTestCase(TestMovies))
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    
    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Özet
    print("\n" + "=" * 70)
    print("TEST ÖZETİ")
    print("=" * 70)
    print(f"Toplam Test: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
