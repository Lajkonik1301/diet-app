from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    pass  
class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    date = models.DateField()
    meal_type = models.CharField(max_length=50)
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"
    
class Recipe(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('supper', 'Supper'),
        ('UNSTOPPABLE MIDNIGHT SWEETS CRAVE', 'UNSTOPPABLE MIDNIGHT SWEETS CRAVE')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # autor przepisu
    name = models.CharField(max_length=100)
    instructions = models.TextField()  # krok po kroku
    calories = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    fat = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()
    meal_type = models.CharField(max_length=40, choices=MEAL_TYPES)
    prep_time = models.PositiveIntegerField(help_text="Time in minutes")  # czas przygotowania

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name