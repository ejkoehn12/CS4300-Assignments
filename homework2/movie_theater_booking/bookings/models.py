from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=255)
    movie_description = models.CharField(max_length=500)
    movie_release_date = models.DateTimeField()
    movie_duration = models.FloatField()


class Seat(models.Model):
    seat_number = models.IntegerField()
    seat_booking_status = models.BooleanField(default=False)

class Booking(models.Model):
    booked_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    booked_seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booked_date = models.DateTimeField()

    

