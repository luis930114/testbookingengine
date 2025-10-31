from django.urls import path
from .views import CheckAvailabilityView

urlpatterns = [
    path('check-availability/', CheckAvailabilityView.as_view(), name='check-availability'),
]
