from django.urls import reverse
from django.test import Client
from behave import given, when, then
from django.contrib.auth.models import User
from bookings.models import Movie
from django.utils import timezone
from datetime import datetime 
@given('There are movies')
def step_movies_exist(context):
      """Ensure there are movies in the database"""
      Movie.objects.create(movie_title='Movie 1', movie_description='Description 1',movie_release_date=timezone.make_aware(datetime(2024, 1, 1, 0, 0, 0)), movie_duration=120)
      Movie.objects.create(movie_title='Movie 2', movie_description='Description 2',movie_release_date=timezone.make_aware(datetime(2024, 1, 1, 0, 0, 0)), movie_duration=90)
      
@given('User has navigated to the homepage')
def step_navigate_to_homepage(context):
      context.client = Client()
      """Navigate to the homepage"""
      home_url = reverse('home')
      context.response = context.client.get(home_url)
      assert context.response.status_code == 200, f"Homepage returned {context.response.status_code}"

@then('the user should be able to see open movies to book')
def step_see_list_of_movies(context):
      """Verify the user sees a list of movies"""
      assert 'movies' in context.response.context, "Movies not found in response context"
      movies = context.response.context['movies']
      assert len(movies) > 0, "No movies found in the list"