from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from place.models import Place, PlaceHall


@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = [
        "id",
        "name_fa",
        "name_en",
        "telephone",
        "created_at",
        "modified_at"
    ]
    autocomplete_fields = ['thumbnail', 'city', 'threads']
    search_fields = ['name_fa', 'name_en', 'telephone']


@admin.register(PlaceHall)
class CinemaHallAdmin(admin.ModelAdmin):
    autocomplete_fields = ['place']
    search_fields = ['place__name_fa', 'place__name_en', 'name']
    list_display = [
        "id",
        "name",
        "created_at",
        "modified_at"
    ]
