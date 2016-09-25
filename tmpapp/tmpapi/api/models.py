from datetime import timedelta, datetime
from uuid import uuid4

from django.db import models
from django.template.defaultfilters import slugify


class ClauseCategory(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        """
        Auto add slug.
        """
        self.slug = slugify(self.name)
        return super(ClauseCategory, self).save(*args, **kwargs)


class Clause(models.Model):
    data_wydania = models.DateField()
    sygnatura_akt = models.CharField(max_length=40)
    nazwa_i_siedziba_sadu_ktory_wydal_wyrok = models.CharField(max_length=100)
    powod = models.CharField(max_length=100)
    pozwani = models.CharField(max_length=100)
    postanowienie_wzorca = models.TextField()
    data_dokonania_wpisu = models.DateField()
    uwagi = models.TextField()
    branza = models.ForeignKey(ClauseCategory)


class Session(models.Model):
    token = models.CharField(max_length=40)
    email = models.EmailField()
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        Auto generate token field.
        """
        if not self.token:
            self.token = str(uuid4())
        if not self.expiration_date:
            self.expiration_date = datetime.today() + timedelta(days=7)
        return super(Session, self).save(*args, **kwargs)


class Image(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE
    )
    path = models.CharField(max_length=128)
    clauses = models.ManyToManyField(Clause, through='FoundClause')


class FoundClause(models.Model):
    """
    Used in m2m relation between Clauses and Images.
    """
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    ocr_data = models.TextField()
