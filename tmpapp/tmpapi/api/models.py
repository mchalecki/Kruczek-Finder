from datetime import timedelta, datetime
from uuid import uuid4

from django.db import models
from django.template.defaultfilters import slugify

from .managers import ClausesManager


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
    data_wydania = models.DateField(null=True)
    sygnatura_akt = models.CharField(max_length=40)
    nazwa_i_siedziba_sadu_ktory_wydal_wyrok = models.CharField(max_length=100)
    powod = models.CharField(max_length=100)
    pozwani = models.CharField(max_length=100)
    postanowienie_wzorca = models.TextField()
    data_dokonania_wpisu = models.DateField(null=True)
    uwagi = models.TextField(null=True)

    category = models.ForeignKey(ClauseCategory)

    objects = ClausesManager()


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
        Session, on_delete=models.CASCADE, null=True
    )
    path = models.CharField(max_length=128)
    clauses = models.ManyToManyField(Clause, through='FoundClause')

    def __str__(self):
        return "Image: %s, FoundClauses: %d" % (self.path, self.clauses.count())


class FoundClause(models.Model):
    """
    Used in m2m relation between Clauses and Images.
    """
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    ocr_data = models.TextField()

    def get_ocr_data(self):
        print(self.ocr_data)
        (p1,p2), (p3,p4) = eval(self.ocr_data)[0]
        x1 = min(p1[0], p2[0], p3[0], p4[0])
        y1 = min(p1[1], p2[1], p3[1], p4[1])
        x2 = max(p1[0], p2[0], p3[0], p4[0])
        y2 = max(p1[1], p2[1], p3[1], p4[1])
        return ("%d,%d,%d,%d" % (x1, y1, x2, y2))
