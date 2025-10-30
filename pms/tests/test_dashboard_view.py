from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
from datetime import date, timedelta
from ..models import Room, Room_type, Customer, Booking
from ..views.views import DashboardView
from unittest.mock import patch

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DashboardViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        # Hoy como referencia
        self.today = date.today()

        # Crear Room_type
        self.room_type = Room_type.objects.create(
            name="Suite",
            price=200.0,
            max_guests=2
        )

        # Crear habitaciones
        self.room1 = Room.objects.create(
            room_type=self.room_type,
            name="101",
            description="Nice room"
        )
        self.room2 = Room.objects.create(
            room_type=self.room_type,
            name="102",
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

    
    @patch('pms.views.views.DashboardService')
    def test_dashboard_view_calculates_occupation_percentage(self, mock_dashboard_service):
        mock_dashboard_service.get_dashboard_data.return_value = {
            'occupied_rooms': 5,
            'total_rooms': 10,
            'occupation_percentage': 50,
        }

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dashboard']['occupation_percentage'], 50)