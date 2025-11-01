from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .booking_service import is_room_available


class AvailabilitySerializer(serializers.Serializer):
    room_id = serializers.IntegerField(required=True)
    checkin = serializers.DateField(required=True, input_formats=["%Y-%m-%d"])
    checkout = serializers.DateField(required=True, input_formats=["%Y-%m-%d"])

    def validate(self, data):
        """Validaciones personalizadas"""
        checkin = data["checkin"]
        checkout = data["checkout"]
        if checkin >= checkout:
            raise serializers.ValidationError("La fecha de salida debe ser posterior a la de entrada.")
        return data


class CheckAvailabilityView(APIView):
    """
    API endpoint para verificar la disponibilidad de una habitación.

    Parámetros de consulta:
        - room_id: ID de la habitación (int)
        - checkin: Fecha de entrada (YYYY-MM-DD)
        - checkout: Fecha de salida (YYYY-MM-DD)

    Respuestas:
        200: Habitación disponible o no disponible
        400: Parámetros inválidos o faltantes
    """
    def get(self, request, *args, **kwargs):
        serializer = AvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        available = is_room_available(
            data["room_id"],
            data["checkin"],
            data["checkout"]
        )

        message = (
            "La habitación está disponible."
            if available else
            "La habitación no está disponible en esas fechas."
        )

        return Response({"available": available, "message": message}, status=status.HTTP_200_OK)