from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta

from pms.models import Booking, Room 

class CheckAvailabilityViewTests(APITestCase):

    def test_missing_params_returns_400(self):
        url = reverse("check-availability")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_format_returns_400(self):
        url = reverse("check-availability")
        response = self.client.get(url, {
            "room_id": 1,
            "checkin": "2024/11/01",
            "checkout": "2024-11-05"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_room_is_available(self):
        room = Room.objects.create(name="Room 1.1")

        url = reverse("check-availability")
        response = self.client.get(url, {
            "room_id": room.id,
            "checkin": "2024-11-01",
            "checkout": "2024-11-05"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["available"])

    def test_room_is_not_available(self):
        room = Room.objects.create(name="Room 1.1")

        Booking.objects.create(
            room=room,
            state=Booking.NEW,
            checkin=date(2024, 11, 2),
            checkout=date(2024, 11, 4),
            guests=2,
            total=150.0,
            code="CD789012",
        )

        url = reverse("check-availability")
        response = self.client.get(url, {
            "room_id": room.id,
            "checkin": "2024-11-01",
            "checkout": "2024-11-05"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["available"])

    def test_checkout_before_checkin_returns_400(self):
        url = reverse("check-availability")
        response = self.client.get(url, {
            "room_id": 1,
            "checkin": "2024-11-10",
            "checkout": "2024-11-05",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
