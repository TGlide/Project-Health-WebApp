from django.db import models
from datetime import datetime

class Nutrition(models.Model):
    patient = models.ForeignKey("users.Patient", on_delete=models.CASCADE)
    food_name = models.CharField(max_length=32)
    time = models.TimeField()
    eaten = models.BooleanField()
    icon = models.CharField(max_length=16)  # Breakfast, lunch or dinner  
    # breakfast = models.BooleanField()
    # lunch = models.BooleanField()
    # dinner = models.BooleanField()


    def __str__(self):
        return "Food {} from {}".format(self.food_name, self.patient)
    
    def time_str(self):
        return str(self.time)[:-3]
    
    def past_time(self):
        return datetime.now().time() > self.time


