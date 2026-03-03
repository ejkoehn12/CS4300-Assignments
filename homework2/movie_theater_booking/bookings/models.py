from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=255)
    movie_description = models.CharField(max_length=500)
    movie_release_date = models.DateTimeField()
    movie_duration = models.FloatField()


class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_booking_status = models.BooleanField(default=False)

class Booking(models.Model):
    booked_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    booked_seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booked_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    

