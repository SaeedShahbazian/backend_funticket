from django.test import TestCase

from geo.models import City, Country, Province


def GeoSample(self):
    """ Create Sample Geo ->
    self.country,
    self.province,
    self.city
    """
    self.country = Country(
        name_fa='ایران',
        name_en='iran'
    )
    self.country.save()

    self.province = Province(
        name_fa='تهران',
        name_en='tehran',
        country=self.country
    )
    self.province.save()

    self.city = City(
        name_fa='دماوند',
        name_en='Damavand',
        province=self.province
    )
    self.city.save()
    return self


class GeoTestCase(TestCase):
    def test_geo_create(self):
        GeoSample(self)
        self.assertIsNotNone(self.city, "Test geo city create faild.")
