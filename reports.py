"""
Raporlama modülü
"""

from datetime import datetime
from seating import get_seat_count_by_status


def occupancy_report(showtimes, seat_maps, bookings):
    """Doluluk raporu oluştur"""
    report = {
        'showtimes': [],
        'overall': {
            'total_seats': 0,
            'sold_seats': 0,
            'occupancy_rate': 0.0
        }
    }
    
    total_capacity = 0
    total_sold = 0
    
    for showtime in showtimes:
        showtime_id = showtime['showtime_id']
        seat_map = seat_maps.get(showtime_id)
        
        if not seat_map:
            continue
        
        # Koltuk sayılarını hesapla
        seat_counts = get_seat_count_by_status(seat_map)
        capacity = sum(seat_counts.values())
        sold = seat_counts.get('sold', 0)
        
        occupancy_rate = (sold / capacity * 100) if capacity > 0 else 0
        
        showtime_report = {
            'showtime_id': showtime_id,
            'movie_id': showtime['movie_id'],
            'date': showtime['date'],
            'time': showtime['time'],
            'screen': showtime['screen'],
            'capacity': capacity,
            'sold': sold,
            'available': seat_counts.get('available', 0),
            'occupancy_rate': round(occupancy_rate, 2)
        }
        
        report['showtimes'].append(showtime_report)
        total_capacity += capacity
        total_sold += sold
    
    # Genel doluluk oranı
    if total_capacity > 0:
        report['overall']['total_seats'] = total_capacity
        report['overall']['sold_seats'] = total_sold
        report['overall']['occupancy_rate'] = round(total_sold / total_capacity * 100, 2)
    
    return report


def revenue_summary(bookings, period):
    """Gelir özeti oluştur"""
    start_date, end_date = period
    
    # Dönemdeki rezervasyonları filtrele
    period_bookings = []
    for booking in bookings:
        if booking['status'] == 'cancelled':
            continue
        
        booking_date = datetime.strptime(booking['booking_date'].split()[0], '%Y-%m-%d')
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start <= booking_date <= end:
            period_bookings.append(booking)
    
    # İstatistikleri hesapla
    total_revenue = sum(b['total'] for b in period_bookings)
    total_tickets = sum(len(b['seats']) for b in period_bookings)
    total_bookings = len(period_bookings)
    
    avg_ticket_price = total_revenue / total_tickets if total_tickets > 0 else 0
    
    summary = {
        'period': {'start': start_date, 'end': end_date},
        'total_revenue': round(total_revenue, 2),
        'total_bookings': total_bookings,
        'total_tickets': total_tickets,
        'average_ticket_price': round(avg_ticket_price, 2)
    }
    
    return summary


def top_movies(bookings, showtimes, limit=5):
    """En çok gelir getiren filmleri bul"""
    movie_stats = {}
    
    # Seans ID -> Film ID eşlemesi
    showtime_to_movie = {}
    for showtime in showtimes:
        showtime_to_movie[showtime['showtime_id']] = showtime['movie_id']
    
    # İstatistikleri topla
    for booking in bookings:
        if booking['status'] == 'cancelled':
            continue
        
        showtime_id = booking['showtime_id']
        movie_id = showtime_to_movie.get(showtime_id)
        
        if movie_id:
            if movie_id not in movie_stats:
                movie_stats[movie_id] = {'revenue': 0.0, 'tickets': 0, 'bookings': 0}
            
            movie_stats[movie_id]['revenue'] += booking['total']
            movie_stats[movie_id]['tickets'] += len(booking['seats'])
            movie_stats[movie_id]['bookings'] += 1
    
    # Listeye çevir ve sırala
    top_list = []
    for movie_id, stats in movie_stats.items():
        top_list.append({
            'movie_id': movie_id,
            'revenue': round(stats['revenue'], 2),
            'tickets_sold': stats['tickets'],
            'bookings': stats['bookings']
        })
    
    top_list.sort(key=lambda x: x['revenue'], reverse=True)
    return top_list[:limit]


def peak_days_analysis(bookings):
    """En yoğun günleri analiz et"""
    day_stats = {}
    
    for booking in bookings:
        if booking['status'] == 'cancelled':
            continue
        
        date = booking['booking_date'].split()[0]
        
        if date not in day_stats:
            day_stats[date] = {'bookings': 0, 'tickets': 0, 'revenue': 0.0}
        
        day_stats[date]['bookings'] += 1
        day_stats[date]['tickets'] += len(booking['seats'])
        day_stats[date]['revenue'] += booking['total']
    
    # Listeye çevir ve sırala
    peak_days = []
    for date, stats in day_stats.items():
        peak_days.append({
            'date': date,
            'bookings': stats['bookings'],
            'tickets': stats['tickets'],
            'revenue': round(stats['revenue'], 2)
        })
    
    peak_days.sort(key=lambda x: x['revenue'], reverse=True)
    
    return {
        'total_days': len(day_stats),
        'peak_days': peak_days[:10]
    }


def showtime_performance_report(showtimes, seat_maps, bookings, showtime_id):
    """Seans performans raporu"""
    # Seansı bul
    showtime = None
    for st in showtimes:
        if st['showtime_id'] == showtime_id:
            showtime = st
            break
    
    if not showtime:
        return {'error': 'Seans bulunamadı'}
    
    seat_map = seat_maps.get(showtime_id)
    if not seat_map:
        return {'error': 'Koltuk haritası bulunamadı'}
    
    # Koltuk bilgilerini al
    seat_counts = get_seat_count_by_status(seat_map)
    capacity = sum(seat_counts.values())
    sold = seat_counts.get('sold', 0)
    occupancy_rate = (sold / capacity * 100) if capacity > 0 else 0
    
    # Rezervasyon bilgilerini al
    showtime_bookings = [b for b in bookings 
                        if b['showtime_id'] == showtime_id and b['status'] != 'cancelled']
    
    total_revenue = sum(b['total'] for b in showtime_bookings)
    avg_booking_value = total_revenue / len(showtime_bookings) if showtime_bookings else 0
    
    return {
        'showtime_id': showtime_id,
        'movie_id': showtime['movie_id'],
        'date': showtime['date'],
        'time': showtime['time'],
        'screen': showtime['screen'],
        'capacity': capacity,
        'seats_sold': sold,
        'occupancy_rate': round(occupancy_rate, 2),
        'total_bookings': len(showtime_bookings),
        'total_revenue': round(total_revenue, 2),
        'average_booking_value': round(avg_booking_value, 2)
    }


def export_report(report, filename):
    """Raporu dosyaya kaydet"""
    import json
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    return filename
