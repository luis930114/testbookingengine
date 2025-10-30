from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Booking, Customer


class RoomSearchForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout', 'guests']
        labels = {
            "guests": "Huéspedes"
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date', 'min': datetime.today().strftime('%Y-%m-%d')}),
            'checkout': forms.DateInput(
                attrs={'type': 'date', 'max': datetime.today().replace(month=12, day=31).strftime('%Y-%m-%d')}),
            'guests': forms.DateInput(attrs={'type': 'number', 'min': 1, 'max': 4}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {
            "name": "Nombre y apellido",
            "phone": "Teléfono"
        }


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests': forms.HiddenInput()
        }


class BookingFormExcluded(ModelForm):
    class Meta:
        model = Booking
        exclude = ["customer", "room", "code"]
        labels = {
        }
        widgets = {
            'checkin': forms.HiddenInput(),
            'checkout': forms.HiddenInput(),
            'guests': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            'state': forms.HiddenInput(),
        }

class BookingDatesForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['checkin', 'checkout']
        labels = {
            "checkin": "Fecha de entrada",
            "checkout": "Fecha de salida"
        }
        widgets = {
            'checkin': forms.DateInput(attrs={'type': 'date'}),
            'checkout': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """
        Valida:
         - checkin < checkout
         - que no haya conflictos con otras reservas 'NEW' para la misma habitación
        """
        cleaned = super().clean()
        checkin = cleaned.get('checkin')
        checkout = cleaned.get('checkout')

        if not checkin or not checkout:
            return cleaned  # dejar que required maneje esto

        if checkin >= checkout:
            raise ValidationError("La fecha de salida debe ser posterior a la fecha de entrada")

        # Si la instancia no tiene room definido, no podemos comprobar disponibilidad
        booking_instance = getattr(self, 'instance', None)
        room = getattr(booking_instance, 'room', None)
        if room is None:
            # No es responsabilidad del form decidir esto, pero notificamos.
            raise ValidationError("No se pudo validar disponibilidad: la reserva no tiene habitación asignada")

        # Conflicto: cualquier booking NEW que se solape.
        conflict_exists = Booking.objects.filter(
            room=room,
            state=Booking.NEW,
            checkin__lt=checkout,
            checkout__gt=checkin
        ).exclude(id=booking_instance.id if booking_instance else None).exists()

        if conflict_exists:
            raise ValidationError("No hay disponibilidad para las fechas seleccionadas")

        return cleaned
