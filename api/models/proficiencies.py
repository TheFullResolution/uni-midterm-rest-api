from django.db import models


class Proficiency(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name
