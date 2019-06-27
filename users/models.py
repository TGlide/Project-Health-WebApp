from django.db import models


class Caregiver(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=256)

    def __str__(self):
        return "Caregiver {}".format(self.name)
    
    def has_patients(self):
        return len(self.patient_set.all())

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': "hidden",
        }

class Patient(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=256)
    age = models.IntegerField()

    def __str__(self):
        return "Patient {}".format(self.name)
    
    def to_dict(self):
        return {
            'caregiver': str(self.caregiver),
            'name': self.name,
            'email': self.email,
            'password': "hidden",
            'age': self.age
        }
