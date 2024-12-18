from django.db import models


class School(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Spell(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    attack_type = models.CharField(max_length=50, null=True, blank=True)
    casting_time = models.CharField(max_length=100)
    concentration = models.BooleanField()
    duration = models.CharField(max_length=100)
    material = models.TextField(null=True, blank=True)
    range = models.CharField(max_length=100)
    ritual = models.BooleanField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="spells")

    def __str__(self):
        return self.name


class SpellDescription(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name="descriptions")
    value = models.TextField()
