from django.test import TestCase
from django.urls import reverse
from pms.models import Room, Room_type
from django.test import override_settings

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RoomNameSearchViewTest(TestCase):
    
    def setUp(self):
        # Creamos un tipo de habitación para asociarlo a las habitaciones
        room_type = Room_type.objects.create(
            name="Doble",
            price=50.0,
            max_guests=2
        )

        Room.objects.create(name="Room 2.1", description="Desc A", room_type=room_type)
        Room.objects.create(name="Room 2.2", description="Desc B", room_type=room_type)

        self.url = reverse("rooms")

    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_room_list_without_search(self):
        response = self.client.get(self.url)
        rooms = response.context["rooms"]
        print(f"Rooms in page: {response}")
        self.assertEqual(len(rooms), 2)  

    def test_filter_room_by_name(self):
        response = self.client.get(self.url + "?name=Room 2.1")
        rooms = response.context["rooms"]
        
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].name, "Room 2.1")

