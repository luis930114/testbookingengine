from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Booking, Room
from datetime import datetime

class CheckAvailabilityView(APIView):
    def get(self, request, *args, **kwargs):
        room_id = request.query_params.get("room_id")
        checkin = request.query_params.get("checkin")
        checkout = request.query_params.get("checkout")

        if not all([room_id, checkin, checkout]):
            return Response({"error": "Faltan parámetros"}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir fechas
        try:
            checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
            checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar disponibilidad
        overlapping = Booking.objects.filter(
            room_id=room_id,
            state=Booking.NEW,
            checkin__lt=checkout_date,
            checkout__gt=checkin_date
        ).exists()

        if overlapping:
            return Response({"available": False, "message": "La habitación no está disponible en esas fechas."})
        return Response({"available": True, "message": "La habitación está disponible."})
