from django.test import TestCase
from .models import Movie, Seat, Booking
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import datetime
# Create your tests here.

class MovieTestApps(TestCase):
      #Creating a testing account
      def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.client = APIClient()
            self.client.force_authenticate(user=self.user)

            self.movie = Movie.objects.create(
                  movie_title='Test Movie',
                  movie_description='A test movie',
                  movie_release_date=timezone.make_aware(datetime(2024, 1, 1, 0, 0)),
                  movie_duration=120
            )

            self.seat = Seat.objects.create(
                  movie=self.movie,
                  seat_number='S1',
                  seat_booking_status=False
            )

      def test_create_booking(self):
        response = self.client.post('/api/bookings/', {
            'booked_seat': self.seat.id,
            'booked_date': timezone.now().isoformat()
        }, format='json')


      #Test to make sure that logging in using wrong credentials fails
      def test_login_with_wrong_credentials(self):
            login_successful = self.client.login(username='wronguser', password='wrongpassword')
            self.assertFalse(login_successful)
      #Test case to make sure that accessing restricted pages without logging in redirects to login page
      def test_access_restricted_page_without_login(self):
            response = self.client.get('/booking-history/')
            self.assertEqual(response.status_code, 302)  # Redirect to login page
            self.assertIn('/accounts/login/', response.url)
      #Test case to make sure homepage is accessible
      def test_homepage_accessible(self):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
      #Test case to make sure bookings history page is accessible
      def test_bookings_page_accessible(self):
            login_successful = self.client.login(username='testuser', password='testpassword')
            self.assertTrue(login_successful)
            response = self.client.get('/booking-history/')
            self.assertEqual(response.status_code, 200)
      #Test case to make sure login page is accessible
      def test_login_page_accessible(self):
            response = self.client.get('/accounts/login/')
            self.assertEqual(response.status_code, 200)
      #Test case to make sure signup page is accessible
      def test_signup_page_accessible(self):
            response = self.client.get('/accounts/signup/')
            self.assertEqual(response.status_code, 200)
      #Test case to test that adding movies works correctly
      def test_add_movie(self):
            response = self.client.post('/api/movies/', {
                  'movie_title': 'Test Movie',
                  'movie_description': 'This is a test movie.',
                  'movie_release_date': '2024-01-01T00:00',
                  'movie_duration': 120,
            })
            self.assertEqual(response.status_code, 201)
            self.assertTrue(Movie.objects.filter(movie_title='Test Movie').exists())
      #Test case to test that removing movies works correctly
      def test_remove_movie(self):
            movie = Movie.objects.create(movie_title='ToBeDeletedMovie', movie_description='This is a test movie.', movie_release_date='2024-01-01T00:00', movie_duration=120)
            response = self.client.delete(f'/api/movies/{movie.id}/')
            self.assertEqual(response.status_code, 204)
            self.assertFalse(Movie.objects.filter(movie_title='ToBeDeletedMovie').exists())
      #Test case to test that booking seats works correctly
      def test_create_booking(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/bookings/', {
            'booked_seat_id': self.seat.id,
            'booked_movie_id': self.movie.id,
            'booked_date': timezone.now().isoformat(),
            'user': self.user.id
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(user=self.user, booked_seat=self.seat).exists())
     #Test case to test that booking an already booked seat fails
      def test_booking_already_booked_seat(self):
        self.client.force_login(self.user)
        response1 = self.client.post('/api/bookings/', {
            'booked_seat_id': self.seat.id,
            'booked_movie_id': self.movie.id,
            'booked_date': timezone.now().isoformat(),
            'user': self.user.id
        }, format='json')
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.post('/api/bookings/', {
            'booked_seat_id': self.seat.id,
            'booked_movie_id': self.movie.id,
            'booked_date': timezone.now().isoformat(),
            'user': self.user.id
        }, format='json')
        self.assertEqual(response2.status_code, 400)
      #Test case to test that try to book a seat without required fields fails
      def test_booking_without_required_fields(self):
            self.client.force_login(self.user)
            response = self.client.post('/api/bookings/', {
                  'booked_seat_id': self.seat.id,
                  'booked_date': timezone.now().isoformat(),
                  'user': self.user.id
            }, format='json')
            self.assertEqual(response.status_code, 400)
      #Test case to test that trying to book with invalid movie or seat id fails
      def test_booking_with_invalid_movie_or_seat_id(self):
            self.client.force_login(self.user)
            response = self.client.post('/api/bookings/', {
                  'booked_seat_id': 9999,  # Invalid seat ID
                  'booked_movie_id': 9999,  # Invalid movie ID
                  'booked_date': timezone.now().isoformat(),
                  'user': self.user.id
            }, format='json')
            self.assertEqual(response.status_code, 400)
      #Test case to make sure that a seat cannot become double booked through the API
      def test_double_booking_prevention(self):
        self.client.force_login(self.user)
        response1 = self.client.post('/api/bookings/', {
            'booked_seat_id': self.seat.id,
            'booked_movie_id': self.movie.id,
            'booked_date': timezone.now().isoformat(),
            'user': self.user.id
        }, format='json')
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.post('/api/bookings/', {
            'booked_seat_id': self.seat.id,
            'booked_movie_id': self.movie.id,
            'booked_date': timezone.now().isoformat(),
            'user': self.user.id
        }, format='json')
        self.assertEqual(response2.status_code, 400)
      #Test case to make sure that api is able to return list of movies correctly
      def test_get_movies_list(self):
            response = self.client.get('/api/movies/')
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.data, list)
      #Test case to make sure that api is able to retrieve a single movie
      def test_get_single_movie(self):
            response = self.client.get(f'/api/movies/{self.movie.id}/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['movie_title'], self.movie.movie_title)
      #Test case to make sure that api is able to update movie
      def test_update_movie(self):
            response = self.client.put(f'/api/movies/{self.movie.id}/', {
                  'movie_title': 'Updated Movie Title',
                  'movie_description': self.movie.movie_description,
                  'movie_release_date': self.movie.movie_release_date.isoformat(),
                  'movie_duration': self.movie.movie_duration,
            }, format='json')
            self.assertEqual(response.status_code, 200)
            self.movie.refresh_from_db()
            self.assertEqual(self.movie.movie_title, 'Updated Movie Title')
      #Test case to make sure that seat movie mismatch is handled correctly when trying to book a seat
      def test_seat_movie_mismatch_on_booking(self):
            self.client.force_login(self.user)
            other_movie = Movie.objects.create(
                  movie_title='Other Movie',
                  movie_description='Another test movie',
                  movie_release_date=timezone.make_aware(datetime(2024, 1, 2, 0, 0)),
                  movie_duration=90
            )
            response = self.client.post('/api/bookings/', {
                  'booked_seat_id': self.seat.id,
                  'booked_movie_id': other_movie.id,
                  'booked_date': timezone.now().isoformat(),
                  'user': self.user.id
            }, format='json')
            self.assertEqual(response.status_code, 400)
      #Test case to make sure a users booking history is returned correctly by the API
      def test_get_booking_history(self):
            self.client.force_login(self.user)
            booking = Booking.objects.create(
                  booked_movie=self.movie,
                  booked_seat=self.seat,
                  booked_date=timezone.now(),
                  user=self.user
            )
            response = self.client.get('/api/bookings/')
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.data, list)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['id'], booking.id)

      


