from django.db import models

from .apps import ApiConfig

class ClausesManager(models.Manager):
    """
    Interface for clauses objects.
    """

    def get_category(self, **kwargs):
    	return self.get_clausecategory_model().objects.get(**kwargs)

    def get_clausecategory_model(self):
        """
        Fucked up import here:
        	- to prevent recursive import
        	- because models.get_model is deprecated
        	- we have no time.
        """
        from .models import ClauseCategory
        return ClauseCategory

    def get_categories(self):
        # using get_model to prevent recursion
        return self.get_clausecategory_model().objects.all()

    def data_for_category(self, category):
        """
        Return list of clauses from given category.
        """
        if isinstance(category, self.get_clausecategory_model()):
            qs = self.filter(category=category)
        if isinstance(category, str):
            qs = self.filter(category__slug=category)
            if not qs.exists():
                qs = self.filter(category__name=category)
        return qs

    def data_for_categories(self, categories):
        """
        Return list of clauses from given categories.
        """
        qs = self.none()
        for category in categories:
            qs = qs | self.data_for_category(category)
        return qs
