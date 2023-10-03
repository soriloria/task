from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# model of user for authenticate
class User(AbstractUser):
    name = models.CharField(max_length=70, unique=True)
    password = models.CharField(max_length=150)
    username = None

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []


# model for restaurants
class Restaurant(models.Model):
    name = models.CharField(max_length=30, unique=True)
    address = models.TextField(max_length=120, unique=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


# menu model with FK with Restaurant
class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    first = models.CharField(max_length=50)
    second = models.CharField(max_length=50)
    drinks = models.CharField(max_length=100)

    class Meta:
        unique_together = [['restaurant', 'day_of_week']]

    def __str__(self):
        return f'Menu for {self.restaurant.name} on {self.day_of_week}'


# model for Votes to count for restaurant
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

