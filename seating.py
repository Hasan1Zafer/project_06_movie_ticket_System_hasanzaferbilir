"""
Koltuk haritası yönetimi modülü
"""


def initialize_seat_map():
    """Koltuk haritası oluştur (8 sıra x 12 koltuk)"""
    rows = 8
    seats_per_row = 12
    premium_rows = ['A', 'B']  # A ve B sıraları premium
    
    row_labels = [chr(65 + i) for i in range(rows)]  # A, B, C, ...
    
    seat_map = {
        'config': {
            'rows': rows,
            'seats_per_row': seats_per_row,
            'premium_rows': premium_rows
        },
        'seats': {}
    }
    
    for row in row_labels:
        for seat_num in range(1, seats_per_row + 1):
            seat_code = f"{row}{seat_num}"
            seat_map['seats'][seat_code] = {
                'status': 'available',
                'zone': 'premium' if row in premium_rows else 'standard',
                'row': row,
                'number': seat_num
            }
    
    return seat_map


def render_seat_map(seat_map):
    """Koltuk haritasını ekrana yazdır"""
    config = seat_map['config']
    seats = seat_map['seats']
    
    rows = config['rows']
    seats_per_row = config['seats_per_row']
    row_labels = [chr(65 + i) for i in range(rows)]
    
    # Başlık
    output = "\n" + "=" * 60 + "\n"
    output += "                         PERDE\n"
    output += "=" * 60 + "\n\n"
    output += "Açıklama: [M] Müsait  [D] Dolu\n\n"
    
    # Kolon numaraları
    output += "    "
    for i in range(1, seats_per_row + 1):
        output += f"{i:3d} "
    output += "\n"
    
    # Koltuk ızgarası
    for row in row_labels:
        output += f"{row}  "
        for seat_num in range(1, seats_per_row + 1):
            seat_code = f"{row}{seat_num}"
            seat_info = seats.get(seat_code, {})
            status = seat_info.get('status', 'available')
            
            symbol = '[M]' if status == 'available' else '[D]'
            output += f"{symbol} "
        
        # Bölge göstergesi
        zone = seats.get(f"{row}1", {}).get('zone', 'standard')
        zone_tr = 'PREMIUM' if zone == 'premium' else 'STANDART'
        output += f"  ({zone_tr})\n"
    
    output += "\n"
    return output


def is_seat_available(seat_map, seat_code):
    """Koltuk müsait mi kontrol et"""
    seats = seat_map['seats']
    seat_info = seats.get(seat_code)
    
    if not seat_info:
        return False
    
    return seat_info['status'] == 'available'


def reserve_seat(seat_map, seat_code):
    """Koltuğu rezerve et (dolu olarak işaretle)"""
    seats = seat_map['seats']
    
    if seat_code not in seats:
        raise ValueError(f"Geçersiz koltuk kodu: {seat_code}")
    
    seat_info = seats[seat_code]
    
    if seat_info['status'] != 'available':
        raise ValueError(f"Koltuk {seat_code} müsait değil!")
    
    seat_info['status'] = 'sold'
    return seat_info


def release_seat(seat_map, seat_code):
    """Koltuğu serbest bırak"""
    seats = seat_map['seats']
    
    if seat_code not in seats:
        raise ValueError(f"Geçersiz koltuk kodu: {seat_code}")
    
    seat_info = seats[seat_code]
    seat_info['status'] = 'available'
    return seat_info


def get_seat_zone(seat_map, seat_code):
    """Koltuğun fiyat bölgesini al"""
    seats = seat_map['seats']
    seat_info = seats.get(seat_code, {})
    return seat_info.get('zone', 'standard')


def get_available_seats(seat_map):
    """Müsait koltukları listele"""
    seats = seat_map['seats']
    return [code for code, info in seats.items() if info['status'] == 'available']


def get_seat_count_by_status(seat_map):
    """Durumlara göre koltuk sayılarını al"""
    seats = seat_map['seats']
    counts = {'available': 0, 'sold': 0}
    
    for seat_info in seats.values():
        status = seat_info.get('status', 'available')
        counts[status] = counts.get(status, 0) + 1
    
    return counts


def validate_seat_code(seat_map, seat_code):
    """Koltuk kodu geçerli mi kontrol et"""
    return seat_code in seat_map['seats']
