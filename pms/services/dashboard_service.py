#from datetime import date
from django.db.models import Sum
from pms.models import Booking, Room

class DashboardService:
    @staticmethod
    def get_dashboard_data():
        new_bookings = Booking.objects.created_today().count()
        incoming = Booking.objects.checkin_today().count()
        outcoming = Booking.objects.checkout_today().count()
        invoiced = Booking.objects.created_today().active().aggregate(
            total=Sum('total')
        )["total"] or 0

        total_rooms = Room.objects.count() or 0
        total_confirmed = Booking.objects.confirmed_today().count()
        percentage_occupation = (
            (total_confirmed / total_rooms) * 100 if total_rooms else 0
        )

        return {
            "new_bookings": new_bookings,
            "incoming_guests": incoming,
            "outcoming_guests": outcoming,
            "invoiced": invoiced,
            "percentage_occupation": percentage_occupation,
            "total_rooms": total_rooms,
            "total_confirmed": total_confirmed
        }
