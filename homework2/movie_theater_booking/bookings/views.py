from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.template import loader
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on movies.
    
    Provides endpoints:
    - GET /api/movies/ - List all movies
    - POST /api/movies/ - Create a new movie
    - GET /api/movies/{id}/ - Retrieve a specific movie
    - PUT /api/movies/{id}/ - Update a movie
    - DELETE /api/movies/{id}/ - Delete a movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for seat management with availability and booking information.
    
    Provides endpoints:
    - GET /api/seats/ - List all seats
    - POST /api/seats/ - Create a new seat
    - GET /api/seats/{id}/ - Retrieve a specific seat
    - PUT /api/seats/{id}/ - Update a seat
    - DELETE /api/seats/{id}/ - Delete a seat
    - GET /api/seats/available/ - Get all available seats
    - GET /api/seats/booked/ - Get all booked seats
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    @action(detail=False, methods=['get'])
    def get_available_seats(self, request):
        """Get all available (unbooked) seats"""
        available_seats = Seat.objects.filter(seat_booking_status=False)
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_booked_seats(self, request):
        """Get all booked seats"""
        booked_seats = Seat.objects.filter(seat_booking_status=True)
        serializer = self.get_serializer(booked_seats, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for users to book seats and view their booking history.
    
    Provides endpoints:
    - GET /api/bookings/ - List all bookings
    - POST /api/bookings/ - Create a new booking
    - GET /api/bookings/{id}/ - Retrieve a specific booking
    - PUT /api/bookings/{id}/ - Update a booking
    - DELETE /api/bookings/{id}/ - Delete a booking
    - GET /api/bookings/history/ - Get booking history
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new booking and automatically mark the seat as booked.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Mark seat as booked when booking is created
        seat = serializer.validated_data['booked_seat']
        if seat.seat_booking_status:
            return Response(
                {"error": "Seat is already booked"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        seat.seat_booking_status = True
        seat.save()
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get booking history for all bookings"""
        bookings = Booking.objects.all()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

def render_home_page(request):
    """Render the home page with current movies list"""
    movies = Movie.objects.all()
    context = {
        "year": timezone.now().year,
        "movies": movies,
    }
    return render(request, 'homepage.html', context)
def render_movies_page(request):
    """Render the movies page with current movies list"""
    movies = Movie.objects.all()
    context = {
        "movies": movies,
    }
    return render(request, 'movie_list.html', context)
def render_booking_history_page(request):
    """Render the booking history page with all bookings"""
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings,
    }
    return render(request, 'booking_history.html', context)
def render_booking_page(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    available_seats = SeatViewSet().get_available_seats(request).data
    taken_seats = SeatViewSet().get_booked_seats(request).data
    context = {
        "movie": movie,
        "available_seats": available_seats,
        "taken_seats": taken_seats,
    }
    return render(request, 'seat_booking.html', context)
def render_login_page(request):
    return render(request, 'registration/login.html')
def render_signup_page(request):
    return render(request, 'registration/signup.html')


def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        duration = request.POST.get('duration')
        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            duration=duration
        )
        return HttpResponse(f'Movie "{movie.title}" added successfully')
def remove_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('id')
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return HttpResponse(f'Movie "{movie.title}" removed successfully')
        except Movie.DoesNotExist:
            return HttpResponse('Movie not found', status=404)