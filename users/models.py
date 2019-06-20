from django.db import models


class Caregiver(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=256)


class Patient(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=256)
