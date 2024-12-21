from django.db import models


# Represents a proficiency associated with a character, class, or other entity in the application.
class Proficiency(models.Model):
    # Unique identifier for the proficiency, used as a reference in the system.
    index = models.CharField(max_length=50, unique=True)
    # Name of the proficiency, e.g., "Light Armor" or "Athletics".
    name = models.CharField(max_length=100)
    # Type of the proficiency, e.g., "Skill", "Armor", or "Tool".
    type = models.CharField(max_length=50)

    def __str__(self):
        # Returns the name of the proficiency when represented as a string.
        return self.name
