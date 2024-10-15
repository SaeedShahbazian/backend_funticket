# import logging

from rest_framework import status
from rest_framework.response import Response

from geo import serializers
from django.contrib.gis.geos import Point
from geo.models import Country, Province, City

# logger = logging.getLogger('mrz')


def country_list(serializer: serializers.GetCountryListSerializer) -> Response:
    countries = Country.list(serializer.validated_data)

    return Response(
        {
            "items": serializers.ResponseCountry(
                countries, many=True,
            ).data,
            "count": countries.count()
        },
        status=status.HTTP_200_OK
    )


def province_list(serializer: serializers.GetProvinceListSerializer) -> Response:
    provinces = Province.list(serializer.validated_data)

    return Response(
        {
            "items": serializers.ResponseProvince(
                provinces, many=True,
            ).data,
            "count": provinces.count()
        },
        status=status.HTTP_200_OK
    )


def city_list(serializer: serializers.GetCityListSerializer) -> Response:
    cities = City.list(serializer.validated_data)

    return Response(
        {
            "items": serializers.ResponseCity(
                cities, many=True,
            ).data,
            "count": cities.count()
        },
        status=status.HTTP_200_OK
    )


def current_location(serializer: serializers.GetLocationCurrentSerializer) -> Response:
    point = Point(
        x=serializer.validated_data['long'],
        y=serializer.validated_data['lat'],
        srid=4326
    )
    city = City.find(
        {
            'point': point
        }
    )
    if not city:
        return Response(
            {
                "message": "Location not found."
            },
            status.HTTP_404_NOT_FOUND
        )
    return Response(
        {
            "city": serializers.ResponseCity(
                city
            ).data,
            "province": serializers.ResponseProvince(
                city.province
            ).data,
            "country": serializers.ResponseCountry(
                city.province.country
            ).data,
        },
        status.HTTP_200_OK
    )
