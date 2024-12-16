from django.db import models


# Main Models
class Class(models.Model):
    index = models.CharField(max_length=50, unique=True)
    hit_die = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Proficiency(models.Model):
    index = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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


# Junction Table Models

class ProficiencyClass(models.Model):
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='proficiency_classes')
    proficiency = models.ForeignKey('Proficiency', on_delete=models.CASCADE, related_name='proficiency_classes')


class ClassProficiency(models.Model):
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class_proficiencies')
    proficiency = models.ForeignKey('Proficiency', on_delete=models.CASCADE, related_name='class_proficiencies')


class ProficiencyRace(models.Model):
    proficiency = models.ForeignKey(Proficiency, on_delete=models.CASCADE, related_name="races_and_subraces")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=True, related_name="proficiencies")
    subrace = models.ForeignKey(Subrace, on_delete=models.CASCADE, null=True, blank=True, related_name="proficiencies")

    def __str__(self):
        return f"{self.proficiency.index} - {self.race or self.subrace}"


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
