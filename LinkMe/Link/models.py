from django.db import models

# Create your models here.
# models.py
# calendar_app/models.py

from django.db import models

class Appointment(models.Model):
    user_id = models.CharField(max_length=100)
    full_time = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Appointment for {self.user_id} on {self.date} from {self.start_time} to {self.end_time}"

