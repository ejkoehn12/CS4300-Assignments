from behave import given, when, then
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from bookings.models import Movie
from django.utils import timezone
from datetime import datetime
@given('User logged into a account')
def step_user_logged_in(context):
      """Create a test user account"""
      context.username = 'testuser'
      context.password = 'testpass123'
      context.user = User.objects.create_user(
            username=context.username,
            password=context.password
      )
      context.client = Client()
      context.login_url = reverse('login') 
      response = context.client.get(context.login_url)
      assert response.status_code == 200, f"Login page returned {response.status_code}"
@given('There are movies to be booked')
def step_movies_available(context):
      Movie.objects.create(movie_title='Movie 1', movie_description='Description 1',movie_release_date=timezone.make_aware(datetime(2024, 1, 1, 0, 0, 0)), movie_duration=120)
      Movie.objects.create(movie_title='Movie 2', movie_description='Description 2',movie_release_date=timezone.make_aware(datetime(2024, 1, 1, 0, 0, 0)), movie_duration=90)
@when('User has clicks on the book button for a movie')
def step_user_clicks_book(context):
      movie = Movie.objects.first() 
      context.movie = movie
      book_url = reverse('booking_page', args=[movie.id])
      context.response = context.client.get(book_url)
      assert context.response.status_code == 200, f"Book page returned {context.response.status_code}"
@then('the user should be able to select a seat')
def step_user_selects_seat(context):
      """Verify the user can select a seat"""
      assert 'seats' in context.response.context, "Seats not found in response context"
      seats = context.response.context['seats']
      assert len(seats) > 0, "No seats available for selection"
@then('the user should be able to click book selected')
def step_user_books_seat(context):
      """Simulate booking a seat"""
      seat = context.response.context['seats'].first()  
      book_url = reverse('booking_page', args=[context.movie.id])
      book_response = context.client.post(book_url, {'booked_seat_id': seat.id, 'booked_movie_id':context.movie.id, 'booked_date': timezone.now().isoformat(), 'user': context.user.id})
      assert book_response.status_code == 200, f"Booking failed with status code {book_response.status_code}"