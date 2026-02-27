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
    path('movies/', views.render_movies_page, name='movie_list'),
    path('booking-history/', views.render_booking_history_page, name='booking_history'),
    path('booking/', views.render_booking_page, name='booking_page'),
    path('booking/<int:movie_id>/', views.render_booking_page, name='booking_page'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]