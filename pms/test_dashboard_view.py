from django.test import TestCase, override_settings
#from django.urls import reverse
from datetime import date, timedelta
from .models import Room, Booking, Room_type, Customer
#from .views import DashboardView

"""@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')

class DashboardViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        # Hoy como referencia
        self.today = date.today()

        # Crear Room_type
        self.room_type = Room_type.objects.create(
            name="Doble",
            price=200.0,
            max_guests=2
        )

        # Crear habitaciones
        self.room1 = Room.objects.create(
            room_type=self.room_type,
            name="Room 1",
            description="Nice room"
        )
        self.room2 = Room.objects.create(
            room_type=self.room_type,
            name="Room 1.2",
            description="Another room"
        )

        # Cliente
        self.customer = Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="123456789"
        )

        # Reserva confirmada que se está hospedando hoy
        Booking.objects.create(
            state="CONF",
            checkin=self.today - timedelta(days=1),
            checkout=self.today + timedelta(days=1),
            room=self.room1,
            guests=2,
            customer=self.customer,
            total=300.0,
            code="B001"
        )

        # Reserva NEW (no cuenta para ocupación)
        Booking.objects.create(
            state="NEW",
            checkin=self.today + timedelta(days=1),
            checkout=self.today + timedelta(days=2),
            room=self.room2,
            guests=1,
            customer=self.customer,
            total=150.0,
            code="B002"
        )

        # Cancelada, tampoco cuenta
        Booking.objects.create(
            state="DEL",
            checkin=self.today - timedelta(days=3),
            checkout=self.today + timedelta(days=1),
            room=self.room2,
            guests=1,
            customer=self.customer,
            total=100.0,
            code="B003"
        )

    def test_dashboard_occupation_percentage(self):
        response = self.client.get(reverse("dashboard"))
        dashboard_data = response.context["dashboard"]       

        # Solo hay 1 booking CONF activo hoy
        expected_percentage = (1 / 2) * 100  

        self.assertEqual(dashboard_data["percentage_occupation"], expected_percentage)
"""

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class BookingQuerySetTests(TestCase):
    def setUp(self):
        # Crear dependencias obligatorias
        self.customer = Customer.objects.create(
            name="John Doe", email="john@example.com", phone="123456789"
        )
        self.room_type = Room_type.objects.create(
            name="Simple", price=100.0, max_guests=2
        )
        self.room = Room.objects.create(
            room_type=self.room_type, name="Room 101", description="Room 101"
        )

        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Reservas para cada escenario
        self.booking_new_today = Booking.objects.create(
            state="NEW",
            checkin=today,
            checkout=tomorrow,
            room=self.room,
            guests=2,
            customer=self.customer,
            total=200.0,
            code="A12345"
        )

        self.booking_deleted = Booking.objects.create(
            state="DEL",
            checkin=yesterday,
            checkout=today,
            room=self.room,
            guests=1,
            customer=self.customer,
            total=100.0,
            code="B67890"
        )

        self.booking_confirmed = Booking.objects.create(
            state="NEW",
            checkin=yesterday,
            checkout=tomorrow,
            room=self.room,
            guests=1,
            customer=self.customer,
            total=150.0,
            code="C11223"
        )

    def test_active_excludes_deleted(self):
        qs = Booking.objects.active()
        self.assertNotIn(self.booking_deleted, qs)
        self.assertIn(self.booking_confirmed, qs)

    def test_created_today_returns_only_today(self):
        self.assertIn(self.booking_confirmed, Booking.objects.created_today())


    def test_checkin_today_filters_correctly(self):
        checkin_today = Booking.objects.checkin_today()
        self.assertIn(self.booking_new_today, checkin_today)

    def test_checkout_today_filters_correctly(self):
        tomorrow = date.today() + timedelta(days=1)
        booking_checkout_today = Booking.objects.create(
            room=self.room,
            guests=1,
            state="NEW",
            checkin=date.today() - timedelta(days=1),
            checkout=tomorrow,
            total=150.0,
            created=date.today()
        )
        # No debe aparecer todavía, ya que el checkout es mañana
        self.assertNotIn(booking_checkout_today, Booking.objects.checkout_today())

    def test_confirmed_today_returns_active_stays(self):
        qs = Booking.objects.confirmed_today()
        self.assertIn(self.booking_confirmed, qs)
