from datetime import date
from django.db import models

class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(state="DEL")

    def created_today(self):
        today = date.today()
        return self.filter(created__date=today)

    def checkin_today(self):
        return self.filter(checkin=date.today()).active()

    def checkout_today(self):
        return self.filter(checkout=date.today()).active()

    def confirmed_today(self):
        today = date.today()
        return self.filter(
            state="CONF",
            checkin__lte=today,
            checkout__gt=today
        )
