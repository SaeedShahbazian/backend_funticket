import json
from django.core.management.base import BaseCommand
from geo.models import Province, City


class Command(BaseCommand):
    help = "Update Farsi Field"

    def handle(self, *args, **kwargs):
        with open('./geo/data/data_farsi.json') as json_file:
            data = json.load(json_file)
            province_update = []
            for item in data['results']:
                province_name_en = item['province']['name_en']
                province_name_fa = item['province']['name_fa']
                city_name_en = item['name_en']
                city_name_fa = item['name_fa']
                if (province_name_fa is not None and province_name_en not in province_update):
                    Province.objects.filter(name_en=province_name_en).update(name_fa=province_name_fa)
                    province_update.append(province_name_en)
                if city_name_fa != '':
                    City.objects.filter(name_en=city_name_en).update(name_fa=city_name_fa)
