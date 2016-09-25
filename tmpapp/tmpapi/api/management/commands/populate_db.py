import csv
from datetime import datetime
from django.core.management.base import BaseCommand

from api.models import Clause, ClauseCategory


class Command(BaseCommand):

    def handle_row(self, row):
        category, _ = ClauseCategory.objects.get_or_create(
            name=row[9]
        )
        try:
            data_wydania = datetime.strptime(
                row[1].split()[0], '%Y-%m-%d'
            )
        except:
            data_wydania = None
        try:
            data_dokonania_wpisu = datetime.strptime(
                row[7].split()[0], '%Y-%m-%d'
            )
        except:
            data_dokonania_wpisu = None

        data = {
            'data_wydania': data_wydania,
            'sygnatura_akt': row[2],
            'nazwa_i_siedziba_sadu_ktory_wydal_wyrok': row[3],
            'powod': row[4],
            'pozwani': row[5],
            'postanowienie_wzorca': row[6],
            'data_dokonania_wpisu': data_dokonania_wpisu,
            'uwagi': row[8],
            'category': category
        }
        Clause.objects.create(**data)

    def handle(self, *args, **kwargs):
        with open('klauzule.csv', 'rt') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                else:
                	self.handle_row(row)
