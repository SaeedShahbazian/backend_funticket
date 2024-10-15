from django.urls import path
from geo.views.panel_views import PanelCitiesList, PanelCurrentLocation

app_name = 'geo_panel'

urlpatterns = [
    path('cities', PanelCitiesList.as_view({'get': 'list'}), name='panel_city_list'),
    path('current', PanelCurrentLocation.as_view(), name='panel_current_location'),
]
