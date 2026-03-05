from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.template import loader
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = []


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = []

    @action(detail=False, methods=['get'])
    #Function to get all available seats for a movie
    def get_available_seats(self, request):
        available_seats = Seat.objects.filter(seat_booking_status=False)
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    #Function to get all booked seats for a movie
    def get_booked_seats(self, request):
        booked_seats = Seat.objects.filter(seat_booking_status=True)
        serializer = self.get_serializer(booked_seats, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = []
    #Function to create a new booking and mark the seat as booked
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_id = serializer.validated_data['booked_movie'].id
        # Mark seat as booked when booking is created
        seat = serializer.validated_data['booked_seat']
        if seat.seat_booking_status:
            return Response(
                {"error": "Seat is already booked"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if seat.movie_id != movie_id:
            return Response(
                {"error": "Seat does not belong to the specified movie"},
                status=status.HTTP_400_BAD_REQUEST
            )
        seat.seat_booking_status = True
        seat.save()
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    #Function to return booking history
    def history(self, request):
        bookings = Booking.objects.all()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

#Helper function to render homepage with required information
def render_home_page(request):
    """Render the home page with current movies list"""
    movies = Movie.objects.all()
    context = {
        "year": timezone.now().year,
        "movies": movies,
    }
    return render(request, 'homepage.html', context)
#Helper Function to render movies page
def render_movies_page(request):
    """Render the movies page with current movies list"""
    movies = Movie.objects.all()
    context = {
        "movies": movies,
    }
    return render(request, 'movie_list.html', context)
@login_required
#Helper function to render booking history page for a logged in user
def render_booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).select_related('booked_movie', 'booked_seat').order_by('-booked_date')
    context = {
        "bookings": bookings,
    }
    return render(request, 'booking_history.html', context)

#Helper function to render login page
def render_login_page(request):
    return render(request, 'registration/login.html')
#Helper function to render signup page
def render_signup_page(request):
    return render(request, 'registration/signup.html')
#Helper function to render seat booking page for a specific movie
@login_required
def render_seat_booking_page(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.filter(movie=movie).order_by('id')
    
    context = {
        "movie": movie,
        "seats": seats,
        "available_seats_count": seats.filter(seat_booking_status=False).count(),
    }
    return render(request, 'seat_booking.html', context)

#Function to add a new movie to the database
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
#Function to remove a movie from the database using movie.id
def remove_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('id')
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return HttpResponse(f'Movie "{movie.title}" removed successfully')
        except Movie.DoesNotExist:
            return HttpResponse('Movie not found', status=404)

from django.utils.dateparse import parse_datetime
from django.utils import timezone
#Function to help with booking one or multiple seats
def book_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.filter(movie=movie).order_by('id')

    if request.method == 'POST':
        # Get selected seats
        seat_ids = request.POST.get("selected_seats", "")
        seat_ids = [int(s) for s in seat_ids.split(",") if s]

        # Get the booking date from the form
        booked_date_str = request.POST.get("booking_date", "")
        booked_date = parse_datetime(booked_date_str)

        # If the form somehow fails to provide a valid date, stop and show an error
        if not booked_date:
            return HttpResponse("Error: Booking date is required and must be valid.", status=400)
        #Looping through all selected seats and setting them as booked 
        for seat_id in seat_ids:
            seat = Seat.objects.get(id=seat_id, movie=movie)
            if not seat.seat_booking_status:
                seat.seat_booking_status = True
                seat.save()
                Booking.objects.create(
                    booked_movie=movie,
                    booked_seat=seat,
                    booked_date=booked_date,
                    user=request.user
                )

        return redirect('seat_booking', movie_id=movie_id)

    context = {
        "movie": movie,
        "seats": seats,
        "available_seats_count": seats.filter(seat_booking_status=False).count(),
        "now": timezone.now(),
    }
    return render(request, 'seat_booking.html', context)
    


