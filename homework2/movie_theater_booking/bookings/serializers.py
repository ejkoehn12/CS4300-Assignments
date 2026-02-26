from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model - handles all movie data"""
    class Meta:
        model = Movie
        fields = ['id', 'movie_title', 'movie_description', 'movie_release_date', 'movie_duration']


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat model - handles seat information and booking status"""
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'seat_booking_status']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model - handles booking information with nested movie and seat data"""
    # Read-only nested serializers to display full movie and seat information
    booked_movie = MovieSerializer(read_only=True)
    booked_seat = SeatSerializer(read_only=True)
    
    # Write-only primary key fields for creating/updating bookings
    booked_movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='booked_movie',
        write_only=True
    )
    booked_seat_id = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        source='booked_seat',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'booked_movie', 'booked_movie_id', 'booked_seat', 'booked_seat_id', 'booked_date']
