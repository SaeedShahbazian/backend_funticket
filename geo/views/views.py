import django_filters.rest_framework
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import filters
from geo import serializers
from geo.controllers import middel
from geo.models import City


class CurrentLocation(APIView):
    """
    This api get current location with lat and long params
    """
    @swagger_auto_schema(
        tags=["Geo"],
        operation_summary='Get Current City and more',
        query_serializer=serializers.GetLocationCurrentSerializer
    )
    def get(self, request, version):
        serializer = serializers.GetLocationCurrentSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return middel.current_location(serializer)


class CitiesList(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This api get list of cities and province
    [api cache 2 Hour]
    """
    serializer_class = serializers.CityListSerializer
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name_fa']
    ordering_fields = ['weigth', 'name_fa', 'province']
    ordering = '-weight'
    queryset = City.objects.select_related('province').all()

    @swagger_auto_schema(
        tags=['Geo'],
        operation_summary='Get city list',
        response={
            200: serializers.CityListSerializer
        },
    )
    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super(CitiesList, self).list(request, *args, **kwargs)
