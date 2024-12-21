from django.db import models


# Represents a school of magic, such as "Evocation" or "Necromancy".
class School(models.Model):
    # Unique identifier for the school, used as a reference in the system.
    index = models.CharField(max_length=50, unique=True)
    # Name of the school, e.g., "Evocation", "Transmutation".
    name = models.CharField(max_length=100)

    def __str__(self):
        # Returns the name of the school when represented as a string.
        return self.name


# Represents a spell, which is a magical ability or effect.
class Spell(models.Model):
    # Unique identifier for the spell, used as a reference in the system.
    index = models.CharField(max_length=50, unique=True)
    # Name of the spell, e.g., "Fireball", "Mage Hand".
    name = models.CharField(max_length=100)
    # Level of the spell, indicating its power or complexity.
    level = models.IntegerField()
    # Type of attack associated with the spell, e.g., "Ranged" or "Melee" (optional).
    attack_type = models.CharField(max_length=50, null=True, blank=True)
    # Casting time required to cast the spell, e.g., "1 action" or "10 minutes".
    casting_time = models.CharField(max_length=100)
    # Indicates if the spell requires concentration to maintain its effects.
    concentration = models.BooleanField()
    # Duration of the spell's effects, e.g., "Instantaneous" or "1 hour".
    duration = models.CharField(max_length=100)
    # Material components required for the spell (optional).
    material = models.TextField(null=True, blank=True)
    # Effective range of the spell, e.g., "60 feet" or "Self".
    range = models.CharField(max_length=100)
    # Indicates if the spell is a ritual spell.
    ritual = models.BooleanField()
    # ForeignKey linking the spell to its associated school of magic. Uses CASCADE to delete spells if the school is deleted.
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="spells")

    def __str__(self):
        # Returns the name of the spell when represented as a string.
        return self.name


# Represents detailed descriptions or effects of a spell.
class SpellDescription(models.Model):
    # ForeignKey linking the description to its associated spell. Uses CASCADE to delete descriptions if the spell is deleted.
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name="descriptions")
    # Detailed textual description of the spell's effects or rules.
    value = models.TextField()

    def __str__(self):
        # Returns a truncated version of the description for readability.
        return f"{self.value[:50]}..." if len(self.value) > 50 else self.value
