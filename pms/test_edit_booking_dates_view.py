from datetime import date, timedelta
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.messages import get_messages

from pms.models import Booking, Room, Room_type, Customer

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditBookingDatesViewTests(TestCase):
    def setUp(self):
        self.room_type = Room_type.objects.create(
            name="Doble",
            price=100.0,
            max_guests=2
        )

        self.room = Room.objects.create(
            name="Room 2.1",
            description="Habitación con vista al mar",
            room_type=self.room_type
        )

        self.customer = Customer.objects.create(
            name="Juan Pérez",
            email="juan@example.com",
            phone="3001234567"
        )

        # Creamos una reserva
        self.booking = Booking.objects.create(
            room=self.room,
            customer=self.customer,
            checkin=date.today(),
            checkout=date.today() + timedelta(days=2),
            guests=2,
            total=200.0,
            code="AB123456",
            state=Booking.NEW
        )

        # URL para editar esta reserva
        self.url = reverse("edit_booking_dates", args=[self.booking.id])

    def test_get_renders_form_successfully(self):
        """Debe renderizar el formulario de edición correctamente."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_booking_dates.html")
        self.assertIn("form", response.context)
        self.assertIn("booking", response.context)

    def test_post_invalid_form_returns_form(self):
        """Debe devolver el formulario si los datos son inválidos."""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_booking_dates.html")

    def test_post_invalid_date_range_adds_error(self):
        """Debe mostrar error si checkout <= checkin."""
        data = {
            "checkin": date.today(),
            "checkout": date.today(),  # misma fecha → inválido
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "La fecha de salida debe ser posterior a la fecha de entrada"
        )

    def test_post_conflict_booking_adds_error(self):
        """Debe mostrar error si existe conflicto de fechas con otra reserva."""
        Booking.objects.create(
            room=self.room,
            customer=self.customer,
            checkin=date.today() + timedelta(days=1),
            checkout=date.today() + timedelta(days=3),
            guests=2,
            total=150.0,
            code="CD789012",
            state=Booking.NEW
        )

        data = {
            "checkin": date.today() + timedelta(days=1),
            "checkout": date.today() + timedelta(days=3),
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay disponibilidad para las fechas seleccionadas")

    def test_post_valid_form_updates_booking_and_redirects(self):
        """Debe actualizar las fechas y redirigir correctamente."""
        new_checkin = date.today() + timedelta(days=5)
        new_checkout = new_checkin + timedelta(days=2)

        data = {
            "checkin": new_checkin,
            "checkout": new_checkout,
        }

        response = self.client.post(self.url, data)

        
        self.booking.refresh_from_db()
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.booking.checkin, new_checkin)
        self.assertEqual(self.booking.checkout, new_checkout)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Fechas actualizadas correctamente" in str(m) for m in messages)
        )
