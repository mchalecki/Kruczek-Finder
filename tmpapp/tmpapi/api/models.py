from django.db import models


class Clauses:
    data_wydania = models.DateField()
    sygnatura_akt = models.CharField(max_length=40)
    nazwa_i_siedziba_sądu_który_wydal_wyrok = models.CharField(max_length=100)
    powod = models.CharField(max_length=100)
    pozwani = models.CharField(max_length=100)
    postanowienie_wzorca = models.TextField()
    data_dokonania_wpisu = models.DateField()
    uwagi = models.TextField()
    branza = models.CharField(max_length=60)
