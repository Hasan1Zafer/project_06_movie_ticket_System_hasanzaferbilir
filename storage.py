"""
Veri kaydetme ve yükleme modülü
"""

import json
import os
from datetime import datetime
import shutil


def load_json(filepath):
    """JSON dosyasından veri yükle"""
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(filepath, data):
    """Veriyi JSON dosyasına kaydet"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_state(base_dir):
    """Tüm sistem verilerini yükle"""
    showtimes_path = os.path.join(base_dir, 'showtimes.json')
    bookings_path = os.path.join(base_dir, 'bookings.json')
    
    showtimes = load_json(showtimes_path)
    bookings = load_json(bookings_path)
    
    # Koltuk haritalarını seanslardan çıkar
    seat_maps = {}
    for showtime in showtimes:
        if 'showtime_id' in showtime and 'seat_map' in showtime:
            seat_maps[showtime['showtime_id']] = showtime['seat_map']
    
    return showtimes, seat_maps, bookings


def save_state(base_dir, showtimes, seat_maps, bookings):
    """Tüm sistem verilerini kaydet"""
    # Koltuk haritalarını seanslara ekle
    for showtime in showtimes:
        if showtime['showtime_id'] in seat_maps:
            showtime['seat_map'] = seat_maps[showtime['showtime_id']]
    
    showtimes_path = os.path.join(base_dir, 'showtimes.json')
    bookings_path = os.path.join(base_dir, 'bookings.json')
    
    save_json(showtimes_path, showtimes)
    save_json(bookings_path, bookings)


def backup_state(base_dir, backup_dir):
    """Verilerin yedeğini al"""
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_files = []
    
    files_to_backup = ['movies.json', 'showtimes.json', 'bookings.json']
    
    for filename in files_to_backup:
        source = os.path.join(base_dir, filename)
        if os.path.exists(source):
            backup_name = f"{filename.replace('.json', '')}_{timestamp}.json"
            destination = os.path.join(backup_dir, backup_name)
            shutil.copy2(source, destination)
            backup_files.append(destination)
    
    return backup_files
