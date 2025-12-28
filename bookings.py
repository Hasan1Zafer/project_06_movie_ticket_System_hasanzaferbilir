"""
Rezervasyon yönetimi modülü
"""

import uuid
from datetime import datetime
import os
from seating import reserve_seat, release_seat, get_seat_zone, is_seat_available


def create_booking(showtimes, seat_maps, booking_data):
    """Yeni rezervasyon oluştur"""
    showtime_id = booking_data['showtime_id']
    seats = booking_data['seats']
    
    # Seansı bul
    showtime = None
    for st in showtimes:
        if st['showtime_id'] == showtime_id:
            showtime = st
            break
    
    if not showtime:
        raise ValueError("Seans bulunamadı!")
    
    # Koltuk haritasını al
    seat_map = seat_maps.get(showtime_id)
    if not seat_map:
        raise ValueError("Koltuk haritası bulunamadı!")
    
    # Tüm koltukların müsait olduğunu kontrol et
    for seat_code in seats:
        if not is_seat_available(seat_map, seat_code):
            raise ValueError(f"Koltuk {seat_code} müsait değil!")
    
    # Toplam fiyatı hesapla (indirimlerle)
    pricing = showtime.get('pricing', {'standard': 10.0, 'premium': 15.0})
    discount_type = booking_data.get('discount_type', 'none')  # 'student', 'group', 'none'
    cost_breakdown = calculate_booking_total(seats, pricing, seat_map, discount_type)
    
    # Koltukları rezerve et
    for seat_code in seats:
        reserve_seat(seat_map, seat_code)
    
    # Rezervasyonu oluştur
    booking = {
        'booking_id': str(uuid.uuid4()),
        'showtime_id': showtime_id,
        'seats': seats,
        'customer_name': booking_data['customer_name'],
        'customer_email': booking_data['customer_email'],
        'customer_phone': booking_data.get('customer_phone', ''),
        'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'subtotal': cost_breakdown['subtotal'],
        'discount': cost_breakdown['discount'],
        'discount_type': cost_breakdown['discount_type'],
        'total': cost_breakdown['total'],
        'status': 'confirmed'
    }
    
    return booking


def cancel_booking(bookings, booking_id, seat_maps):
    """Rezervasyonu iptal et"""
    # Rezervasyonu bul
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    
    if not booking:
        return False
    
    if booking['status'] == 'cancelled':
        print("Rezervasyon zaten iptal edilmiş!")
        return False
    
    # Koltukları serbest bırak
    showtime_id = booking['showtime_id']
    seat_map = seat_maps.get(showtime_id)
    
    if seat_map:
        for seat_code in booking['seats']:
            release_seat(seat_map, seat_code)
    
    # Rezervasyon durumunu güncelle
    booking['status'] = 'cancelled'
    booking['cancelled_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return True


def calculate_booking_total(seats, pricing, seat_map, discount_type='none'):
    """Rezervasyon toplam fiyatını hesapla (indirimlerle)
    
    İndirim tipleri:
    - 'student': Öğrenci indirimi %10
    - 'group': Grup indirimi (4+ koltuk için %15)
    - 'none': İndirim yok
    """
    subtotal = 0.0
    
    # Her koltuğun fiyatını hesapla
    for seat_code in seats:
        zone = get_seat_zone(seat_map, seat_code)
        seat_price = pricing.get(zone, 10.0)
        subtotal += seat_price
    
    # İndirim hesapla
    discount = 0.0
    discount_applied = 'none'
    
    # Grup indirimi (4+ koltuk için %15)
    if len(seats) >= 4:
        discount = subtotal * 0.15  # %15 indirim
        discount_applied = 'group'
    # Öğrenci indirimi (%10)
    elif discount_type == 'student':
        discount = subtotal * 0.10  # %10 indirim
        discount_applied = 'student'
    
    # Toplam hesapla
    total = subtotal - discount
    
    return {
        'subtotal': round(subtotal, 2),
        'discount': round(discount, 2),
        'discount_type': discount_applied,
        'total': round(total, 2)
    }


def list_customer_bookings(bookings, email):
    """Müşterinin rezervasyonlarını listele"""
    return [b for b in bookings if b['customer_email'] == email]


def get_booking(bookings, booking_id):
    """ID'ye göre rezervasyon bul"""
    for booking in bookings:
        if booking['booking_id'] == booking_id:
            return booking
    return None


def generate_ticket(booking, tickets_dir):
    """Bilet oluştur"""
    os.makedirs(tickets_dir, exist_ok=True)
    
    filename = f"ticket_{booking['booking_id'][:8]}.txt"
    filepath = os.path.join(tickets_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write("=" * 50 + "\n")
        f.write("         SİNEMA BİLETİ\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Rezervasyon ID: {booking['booking_id']}\n")
        f.write(f"Müşteri: {booking['customer_name']}\n")
        f.write(f"Koltuklar: {', '.join(booking['seats'])}\n")
        f.write(f"Toplam: ${booking['total']:.2f}\n")
        f.write(f"Tarih: {booking['booking_date']}\n")
        f.write(f"Durum: {booking['status']}\n")
        f.write("\n" + "=" * 50 + "\n")
    
    return filepath
