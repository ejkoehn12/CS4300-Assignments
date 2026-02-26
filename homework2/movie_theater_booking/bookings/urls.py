from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('/movies/', views.render_movies_page, name='movie_list'),
    path('/bookings/', views.render_booking_history, name='booking_history'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path("add-movie/", views.add_movie, name="add_movie"),
    path("remove-movie/", views.remove_movie, name="remove_movie"),
]