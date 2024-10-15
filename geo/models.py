from django.contrib.gis.db import models
from django.db.models import Q


class Country(models.Model):
    name_fa = models.CharField(max_length=100, null=True, blank=True)
    name_en = models.CharField(max_length=100, null=True, blank=True)
    area = models.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name_en or ''

    @classmethod
    def list(cls, data):
        result = cls.objects

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.all()

    @classmethod
    def find(cls, data):
        query = {}
        if 'point' in data:
            query['point__contains'] = data['point']

        result = cls.objects.filter(
            **query
        )

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.first()


class Province(models.Model):
    name_fa = models.CharField(max_length=100, null=True, blank=True)
    name_en = models.CharField(max_length=100, null=True, blank=True)
    area = models.MultiPolygonField(null=True, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='provinces'
    )

    def __str__(self):
        return self.name_en or ''

    @classmethod
    def list(cls, data):
        query = {
            'country_id': data['country_id']
        }
        result = cls.objects.filter(
            **query
        )

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.all()

    @classmethod
    def find(cls, data):
        query = {}
        if 'point' in data:
            query['point__contains'] = data['point']
        else:
            if 'country_id' in data:
                query['country_id'] = data['country_id']

        result = cls.objects.filter(
            **query
        )

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.first()


class City(models.Model):
    name_fa = models.CharField(max_length=100, null=True, blank=True)
    name_en = models.CharField(max_length=100, null=True, blank=True)
    area = models.MultiPolygonField(null=True, blank=True)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='cities'
    )
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.name_en or ''

    @classmethod
    def list(cls, data):
        query = {
            'province_id': data['province_id']
        }

        result = cls.objects.filter(
            **query
        )

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.all()

    @classmethod
    def find(cls, data):
        query = {}
        if 'point' in data:
            query['area__contains'] = data['point']
        else:
            if 'province_id' in data:
                query['province_id'] = data['province_id']
        result = cls.objects.filter(
            **query
        )

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.first()
