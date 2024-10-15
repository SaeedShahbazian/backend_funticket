from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (Country, Province, City)


class CountryResource(resources.ModelResource):

    class Meta:
        model = Country


class ProvinceResource(resources.ModelResource):

    class Meta:
        model = Province


class CityResource(resources.ModelResource):

    class Meta:
        model = City


@admin.register(Country)
class CountryAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    search_fields = ['name_fa', 'name_en']
    list_display = [
        "id",
        "name_fa",
        "name_en"
    ]

    resource_class = CountryResource


@admin.register(Province)
class ProvinceAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    search_fields = ['name_fa', 'name_en', 'country__name_fa', 'country__name_en']
    autocomplete_fields = ['country', ]
    list_display = [
        "id",
        "name_fa",
        "name_en",
        "country"
    ]
    resource_class = ProvinceResource


@admin.register(City)
class CityAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    search_fields = ['name_fa', 'name_en', 'province__name_fa', 'province__name_en']
    autocomplete_fields = ['province', ]
    list_display = [
        "id",
        "name_fa",
        "name_en",
        "province",
    ]
    resource_class = CityResource
