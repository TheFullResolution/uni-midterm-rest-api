from django.db import models


class Race(models.Model):
    index = models.CharField(max_length=50, unique=True)
    age = models.TextField()
    alignment = models.TextField()
    language_desc = models.TextField()
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    size_description = models.TextField()
    speed = models.IntegerField()

    def __str__(self):
        return self.name


class Subrace(models.Model):
    index = models.CharField(max_length=50, unique=True)
    desc = models.TextField()
    name = models.CharField(max_length=100)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="subraces")

    def __str__(self):
        return self.name
