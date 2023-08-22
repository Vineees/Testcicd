from django.db import models
from django.contrib.auth.models import AbstractUser


class MoteType(models.IntegerChoices):
    null = 0, 'NullMote'
    water = 1, 'WMote'
    energy = 2, 'EMote'


class ExtendUser(AbstractUser):
    profile_photo = models.ImageField(
        upload_to='profile/', default='profile/default.png')
    description = models.CharField(max_length=32, blank=True)

    def __str__(self):
        if (self.first_name):
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username


class Motes(models.Model):
    name = models.CharField(max_length=255)
    type = models.IntegerField(default=MoteType.null, choices=MoteType.choices)
    section = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Data(models.Model):
    mote = models.ForeignKey(Motes, on_delete=models.CASCADE, default=0)
    last_collection = models.FloatField(
        default=0)  # Litros/Hora no último minuto
    total = models.FloatField(default=0)  # Listros totais
    collect_date = models.DateTimeField(auto_now_add=True)  # Data de coleta


class StatsHour(models.Model):
    mote = models.ForeignKey(Motes, on_delete=models.CASCADE, blank=True)
    mean = models.FloatField(blank=True)
    median = models.FloatField(blank=True)
    std = models.FloatField(blank=True)
    cv = models.FloatField(blank=True)
    max = models.FloatField(blank=True)
    min = models.FloatField(blank=True)
    fq = models.FloatField(blank=True)
    tq = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
