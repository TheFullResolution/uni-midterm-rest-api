from django.db import models
from .classes import Class
from .proficiencies import Proficiency
from .races import Race, Subrace
from .spells import Spell
from .subclasses import Subclass


# Junction table linking classes and proficiencies.
class ClassProficiency(models.Model):
    # ForeignKey linking the class to its proficiencies.
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class_proficiencies')
    # ForeignKey linking the proficiency to its classes.
    proficiency = models.ForeignKey('Proficiency', on_delete=models.CASCADE, related_name='class_proficiencies')


# Alternative junction table between classes and proficiencies, maintaining additional relationships.
class ProficiencyClass(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='proficiency_classes')
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name='proficiency_classes')


# Represents proficiencies granted by a race or subrace.
class ProficiencyRace(models.Model):
    # ForeignKey linking the proficiency.
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="races_and_subraces")
    # ForeignKey for the race that grants the proficiency.
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True, related_name="proficiencies")
    # ForeignKey for the subrace that grants the proficiency (optional if race already defined).
    subrace = models.ForeignKey(Subrace, on_delete=models.CASCADE, null=True, blank=True, related_name="proficiencies")


# Starting proficiencies provided by a race at character creation.
class RaceStartingProficiency(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="starting_proficiencies")
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="starting_races")


# Starting proficiencies provided by a subrace at character creation.
class SubraceStartingProficiency(models.Model):
    subrace = models.ForeignKey(Subrace, on_delete=models.CASCADE, related_name="starting_proficiencies")
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="starting_subraces")


# Links spells to the classes that can use them.
class SpellClass(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name="classes")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="spells")


# Links spells to the subclasses that can use them.
class SpellSubclass(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name="subclasses")
    subclass = models.ForeignKey(Subclass, on_delete=models.CASCADE, related_name="spells")
