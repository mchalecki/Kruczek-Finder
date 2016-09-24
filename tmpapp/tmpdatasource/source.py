import json
import os
from unipath import Path

from django.template.defaultfilters import slugify


class DataSource(object):
    """
    "Wannabe API" for our app.
    """
    DEFAULT_DATA_FILENAME = Path(__file__).ancestor(1).child('data').child('data.json')

    def __init__(self, data_filename=None):
        if not data_filename:
            data_filename = self.DEFAULT_DATA_FILENAME
        with open(data_filename, 'r') as data_file:
            data = json.loads(data_file.read())

        self.data = {
            slugify(name): {
                'name': name,
                'clauses': clauses
            } for name, clauses in data.items()
        }

    def get_categories(self):
        """
        Returns list of tuples:
        (category_slug, category_full_name)
        """
        return [(slug, data['name']) for slug, data in self.data.items()]

    def data_for_category(self, category):
        """
        Returns list of clauses for given category.
        Returns empty list when category was not found.
        """
        try:
            return self.data[category]['clauses']
        except KeyError:
            return []

    def data_for_categories(self, categories):
        """
        Returns list of clauses for given categories.
        """
        clauses = []
        for category in categories:
            clauses.extend(self.data_for_category(category))
        return clauses
