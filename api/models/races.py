from django.db import models


# Represents a race in the application, such as a fantasy race like "Elf" or "Dwarf".
class Race(models.Model):
    # Unique identifier for the race, used as a reference in the system.
    index = models.CharField(max_length=50, unique=True)
    # Description of the typical age characteristics of the race, such as lifespan or age of maturity.
    age = models.TextField()
    # Description of the general alignment tendencies of the race (e.g., lawful good, chaotic neutral).
    alignment = models.TextField()
    # Details about the languages spoken or understood by the race.
    language_desc = models.TextField()
    # Name of the race, e.g., "Elf", "Human", or "Dwarf".
    name = models.CharField(max_length=100)
    # Size category of the race (e.g., "Medium", "Small").
    size = models.CharField(max_length=50)
    # Detailed description of the size attributes, such as height and weight.
    size_description = models.TextField()
    # Base speed of the race, typically measured in feet per turn or equivalent.
    speed = models.IntegerField()

    def __str__(self):
        # Returns the name of the race when represented as a string.
        return self.name


# Represents a subrace associated with a parent race, such as "High Elf" for the "Elf" race.
class Subrace(models.Model):
    # Unique identifier for the subrace, used as a reference in the system.
    index = models.CharField(max_length=50, unique=True)
    # Detailed description of the subrace, such as unique traits or cultural information.
    desc = models.TextField()
    # Name of the subrace, e.g., "High Elf", "Wood Elf".
    name = models.CharField(max_length=100)
    # ForeignKey linking the subrace to its parent race. Uses CASCADE to delete subraces when the parent race is deleted.
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="subraces")

    def __str__(self):
        # Returns the name of the subrace when represented as a string.
        return self.name
