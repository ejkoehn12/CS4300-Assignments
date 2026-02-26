from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]