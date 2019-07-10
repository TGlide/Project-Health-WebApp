from django.db import models
from datetime import datetime


class Medication(models.Model):
    patient = models.ForeignKey("users.Patient", on_delete=models.CASCADE)
    name = models.CharField(max_length=42)
    dose = models.CharField(max_length=32)
    time = models.TimeField()
    taken = models.BooleanField()

    def __str__(self):
        return "Med {} from {}".format(self.name, self.patient)

    def time_str(self):
        return str(self.time)[:-3]

    def past_time(self):
        return datetime.now().time() > self.time

    def state(self):
        if self.taken:
            return 'taken'
        if self.past_time():
            return 'not_taken'
        return 'awaiting'

    def to_dict(self):
        return {
            'patient': str(self.patient),
            'name': self.name,
            'dose': self.dose,
            'time': self.time,
            'taken': self.taken,
            "id": self.id,
        }
