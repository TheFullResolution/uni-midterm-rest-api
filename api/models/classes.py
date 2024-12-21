from django.db import models


# Represents a class in the application, e.g., a character class in a game.
class Class(models.Model):
    # Unique identifier for the class, used as a reference.
    index = models.CharField(max_length=50, unique=True)
    # Represents the hit die of the class, typically used in role-playing contexts.
    hit_die = models.IntegerField()
    # Name of the class, e.g., "Wizard" or "Fighter".
    name = models.CharField(max_length=100)

    def __str__(self):
        # Returns the name of the class when represented as a string.
        return self.name
