from django.db import models


class Class(models.Model):
    index = models.CharField(max_length=50, unique=True)
    hit_die = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subclass(models.Model):
    index = models.CharField(max_length=50, unique=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subclasses")
    name = models.CharField(max_length=100)
    subclass_flavor = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubclassDescription(models.Model):
    subclass = models.OneToOneField(Subclass, on_delete=models.CASCADE, related_name="description")
    value = models.TextField()
