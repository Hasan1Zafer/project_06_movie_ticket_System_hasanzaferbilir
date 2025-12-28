"""
Film yönetimi ve seans planlama modülü
"""

import json
import os
import uuid


def load_movies(path):
    """Filmleri JSON dosyasından yükle"""
    if not os.path.exists(path):
        return []
    
    with open(path, 'r') as f:
        return json.load(f)


def save_movies(path, movies):
    """Filmleri JSON dosyasına kaydet"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(movies, f, indent=2)


def add_movie(movies, movie_data):
    """Yeni film ekle"""
    movie = {
        'movie_id': str(uuid.uuid4()),
        'title': movie_data['title'],
        'genre': movie_data['genre'],
        'duration': movie_data['duration'],
        'rating': movie_data['rating'],
        'description': movie_data.get('description', ''),
        'active': True
    }
    movies.append(movie)
    return movie


def get_movie(movies, movie_id):
    """ID'ye göre film bul"""
    for movie in movies:
        if movie['movie_id'] == movie_id:
            return movie
    return None


def schedule_showtime(showtimes, showtime_data):
    """Yeni seans planla"""
    from seating import initialize_seat_map
    
    showtime = {
        'showtime_id': str(uuid.uuid4()),
        'movie_id': showtime_data['movie_id'],
        'screen': showtime_data.get('screen', 'Screen 1'),
        'date': showtime_data['date'],
        'time': showtime_data['time'],
        'language': showtime_data.get('language', 'English'),
        'pricing': showtime_data.get('pricing', {
            'standard': 10.0,
            'premium': 15.0
        })
    }
    
    # Koltuk haritası oluştur (8 sıra x 12 koltuk)
    showtime['seat_map'] = initialize_seat_map()
    showtimes.append(showtime)
    return showtime


def list_showtimes(showtimes, movie_id=None):
    """Seansları listele"""
    if movie_id:
        return [s for s in showtimes if s['movie_id'] == movie_id]
    return showtimes


def get_showtime(showtimes, showtime_id):
    """ID'ye göre seans bul"""
    for showtime in showtimes:
        if showtime['showtime_id'] == showtime_id:
            return showtime
    return None


def list_active_movies(movies):
    """Aktif filmleri listele"""
    return [m for m in movies if m.get('active', True)]

