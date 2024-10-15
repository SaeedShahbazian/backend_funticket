from django.urls import path
from .views import CitiesList, CurrentLocation
app_name = 'geo'

urlpatterns = [
    path('cities', CitiesList.as_view({'get': 'list'}), name='city_list'),
    path('current', CurrentLocation.as_view(), name='current_location'),
]
