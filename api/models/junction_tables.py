from django.db import models
from .classes import Class, Subclass
from .proficiencies import Proficiency
from .races import Race, Subrace
from .spells import Spell


class ClassProficiency(models.Model):
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class_proficiencies')
    proficiency = models.ForeignKey('Proficiency', on_delete=models.CASCADE, related_name='class_proficiencies')


class ProficiencyClass(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='proficiency_classes')
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name='proficiency_classes')


class ProficiencyRace(models.Model):
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="races_and_subraces")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True, related_name="proficiencies")
    subrace = models.ForeignKey(Subrace, on_delete=models.CASCADE, null=True, blank=True, related_name="proficiencies")


class RaceStartingProficiency(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="starting_proficiencies")
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="starting_races")


class SubraceStartingProficiency(models.Model):
    subrace = models.ForeignKey(Subrace, on_delete=models.CASCADE, related_name="starting_proficiencies")
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="starting_subraces")


class SpellClass(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name="classes")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="spells")


class SpellSubclass(models.Model):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, related_name="subclasses")
    subclass = models.ForeignKey(Subclass, on_delete=models.CASCADE, related_name="spells")
