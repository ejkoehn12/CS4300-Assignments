from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie, Seat

@receiver(post_save, sender=Movie)
def create_seats_for_movie(sender, instance, created, **kwargs):
    if created:
        # Create 20 Seat objects linked to this movie
        seats_to_create = [
            Seat(movie=instance, seat_number=f"S{num+1}")
            for num in range(20)
        ]
        Seat.objects.bulk_create(seats_to_create)
