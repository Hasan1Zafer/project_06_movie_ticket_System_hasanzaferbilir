"""
Veri doğrulama (validation) modülü
"""

import re
from datetime import datetime


def validate_email(email):
    """Email formatını kontrol et"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Telefon numarasını kontrol et (opsiyonel alan)"""
    if not phone:  # Boş olabilir
        return True
    # 10-11 haneli sayı kontrolü
    pattern = r'^[0-9]{10,11}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None


def validate_date(date_str):
    """Tarih formatını kontrol et (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_time(time_str):
    """Saat formatını kontrol et (HH:MM)"""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False


def validate_seat_code(seat_code):
    """Koltuk kodunu kontrol et (örn: A5, B12)"""
    pattern = r'^[A-H][1-9]$|^[A-H]1[0-2]$'  # A-H sıra, 1-12 numara
    return re.match(pattern, seat_code.upper()) is not None


def validate_name(name):
    """İsim kontrolü (en az 2 karakter)"""
    return len(name.strip()) >= 2


def validate_price(price):
    """Fiyat kontrolü (pozitif sayı)"""
    try:
        p = float(price)
        return p > 0
    except (ValueError, TypeError):
        return False


def validate_duration(duration):
    """Film süresi kontrolü (30-300 dakika arası)"""
    try:
        d = int(duration)
        return 30 <= d <= 300
    except (ValueError, TypeError):
        return False


def validate_rating(rating):
    """Film puanı kontrolü"""
    valid_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17', '7+', '13+', '18+']
    return rating.upper() in valid_ratings
