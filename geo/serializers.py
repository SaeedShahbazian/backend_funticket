from geo.models import Country, Province, City
from rest_framework import serializers


class CountryFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id', 'name_fa', 'name_en']


class ResponseCountry(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "name_fa",
            "name_en",
            "id"
        ]


class ResponseProvince(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = [
            "name_fa",
            "name_en",
            "id"
        ]


class ResponseCity(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "name_fa",
            "name_en",
            "id"
        ]


class GetLocationCurrentSerializer(serializers.Serializer):
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)


class GetCountryListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=50)


class GetProvinceListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    country_id = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=50)


class GetCityListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    province_id = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=50)


class CityListSerializer(serializers.ModelSerializer):
    province = ResponseProvince(many=False)

    class Meta:
        model = City
        fields = [
            "name_fa",
            "name_en",
            "province",
            "id"
        ]
