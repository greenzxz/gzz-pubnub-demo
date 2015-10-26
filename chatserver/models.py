from django.db import models

# Create your models here.
class Channel(models.Model):
    channel_name = models.CharField(max_length=200, primary_key=True)

class Person(models.Model):
    person_name = models.CharField(max_length=200)
    person_key = models.CharField(max_length=200)
    subbed_channels = models.ManyToManyField(Channel)
