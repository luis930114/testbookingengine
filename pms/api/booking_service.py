from ..models import Booking

def is_room_available(room_id, checkin_date, checkout_date):
    """
    Verifica si una habitación está disponible en un rango de fechas dado.

    Args:
        room_id (int): ID de la habitación.
        checkin_date (date): Fecha de entrada.
        checkout_date (date): Fecha de salida.

    Returns:
        bool: True si la habitación está disponible, False si no lo está.
    """
    
    return not Booking.objects.filter(
        room_id=room_id,
        state=Booking.NEW,
        checkin__lt=checkout_date,
        checkout__gt=checkin_date,
    ).exists()