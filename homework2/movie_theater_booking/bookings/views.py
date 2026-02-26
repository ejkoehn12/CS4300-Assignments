from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


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
    def available(self, request):
        """Get all available (unbooked) seats"""
        available_seats = Seat.objects.filter(seat_booking_status=False)
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def booked(self, request):
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
