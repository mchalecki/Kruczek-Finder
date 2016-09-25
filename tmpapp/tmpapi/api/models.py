from django.db import models
from datetime import timedelta, datetime


class Clauses(models.Model):
    data_wydania = models.DateField()
    sygnatura_akt = models.CharField(max_length=40)
    nazwa_i_siedziba_sądu_który_wydal_wyrok = models.CharField(max_length=100)
    powod = models.CharField(max_length=100)
    pozwani = models.CharField(max_length=100)
    postanowienie_wzorca = models.TextField()
    data_dokonania_wpisu = models.DateField()
    uwagi = models.TextField()
    branza = models.CharField(max_length=60)


class Request_Session(models.Model):
    token = models.CharField(max_length=40)
    email = models.EmailField()


class Image(models.Model):
    request_session = models.ForeignKey(Request_Session, on_delete=models.CASCADE)
    image = models.ImageField()
    url = models.CharField(max_length=40)
    expire_date = models.DateTimeField(default=datetime.today() + timedelta(days=7))
