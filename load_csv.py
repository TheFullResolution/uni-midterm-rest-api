import os
import csv
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dndRestAPI.settings')
django.setup()

from dndRestAPI.models import Class, Proficiency, ClassProficiency, Race, ProficiencyClass, ProficiencyRace, \
    RaceStartingProficiency, Subrace, SubraceStartingProficiency, Subclass, SubclassDescription, School, Spell, \
    SpellDescription, SpellClass, SpellSubclass


def load_csv(file_path):
    """
    Generic function to load CSV data into a dictionary.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


def load_classes(file_path):
    """
    Load data from classes.csv into the Class model.
    """
    data = load_csv(file_path)
    for row in data:
        Class.objects.get_or_create(
            index=row['index'],
            defaults={'hit_die': int(row['hit_die']), 'name': row['name']}
        )
    print("Classes loaded.")


def load_proficiencies(file_path):
    """
    Load data from proficiencies.csv into the Proficiency model.
    """
    data = load_csv(file_path)
    for row in data:
        Proficiency.objects.get_or_create(
            index=row['index'],
            defaults={'name': row['name'], 'type': row['type']}
        )
    print("Proficiencies loaded.")


def load_races(file_path):
    """
    Load data from races.csv into the Race model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Race.objects.get_or_create(
                index=row['index'],
                defaults={
                    'age': row['age'],
                    'alignment': row['alignment'],
                    'language_desc': row['language_desc'],
                    'name': row['name'],
                    'size': row['size'],
                    'size_description': row['size_description'],
                    'speed': int(row['speed']),
                }
            )
    print("Races loaded.")


def load_subraces(file_path):
    """
    Load data from subraces.csv into the Subrace model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            race = Race.objects.get(index=row['race_index'])
            Subrace.objects.get_or_create(
                index=row['index'],
                defaults={
                    'desc': row['desc'],
                    'name': row['name'],
                    'race': race,
                }
            )
    print("Subraces loaded.")


def load_subclasses(file_path):
    """
    Load data from subclasses.csv into the Subclass model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_obj = Class.objects.get(index=row['class_index'])
            Subclass.objects.get_or_create(
                index=row['index'],
                defaults={
                    'name': row['name'],
                    'subclass_flavor': row['subclass_flavor'],
                    'class_obj': class_obj,
                }
            )
    print("Subclasses loaded.")


def load_subclasses_desc(file_path):
    """
    Load data from subclasses_desc.csv into the SubclassDescription model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subclass = Subclass.objects.get(index=row['subclasses_index'])
            SubclassDescription.objects.get_or_create(
                subclass=subclass,
                defaults={'value': row['value']}
            )
    print("Subclass Descriptions loaded.")


def load_spells(file_path):
    """
    Load data from spells.csv into the Spell model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            school, _ = School.objects.get_or_create(index=row['school_index'], name=row['school_name'])
            Spell.objects.get_or_create(
                index=row['index'],
                defaults={
                    'name': row['name'],
                    'level': int(row['level']),
                    'attack_type': row['attack_type'] if row['attack_type'] else None,
                    'casting_time': row['casting_time'],
                    'concentration': row['concentration'] == 'True',
                    'duration': row['duration'],
                    'material': row['material'] if row['material'] else None,
                    'range': row['range'],
                    'ritual': row['ritual'] == 'True',
                    'school': school,
                }
            )
    print("Spells loaded.")


def load_spell_descriptions(file_path):
    """
    Load data from spells_desc.csv into the SpellDescription model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spell = Spell.objects.get(index=row['spells_index'])
            SpellDescription.objects.create(spell=spell, value=row['value'])
    print("Spell Descriptions loaded.")


# Junction Table Loaders
def load_class_proficiencies(file_path):
    data = load_csv(file_path)
    for row in data:
        class_obj = Class.objects.get(index=row['classes_index'])
        proficiency = Proficiency.objects.get(index=row['ref_index'])
        ClassProficiency.objects.get_or_create(class_obj=class_obj, proficiency=proficiency)
    print("Class proficiencies loaded.")


def load_proficiencies_classes(file_path):
    """
    Load data from proficiencies_classes.csv into the ProficiencyClass model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proficiency = Proficiency.objects.get(index=row['proficiencies_index'])
            class_obj = Class.objects.get(index=row['ref_index'])
            ProficiencyClass.objects.get_or_create(proficiency=proficiency, class_obj=class_obj)
    print("Proficiencies-Classes loaded.")


def load_proficiencies_races(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proficiency = Proficiency.objects.get(index=row['proficiencies_index'])
            try:
                race = Race.objects.get(index=row['ref_index'])
                ProficiencyRace.objects.create(proficiency=proficiency, race=race)
            except Race.DoesNotExist:
                subrace = Subrace.objects.get(index=row['ref_index'])
                ProficiencyRace.objects.create(proficiency=proficiency, subrace=subrace)
                

def load_races_starting_proficiencies(file_path):
    """
    Load data from races_starting_proficiencies.csv into the RaceStartingProficiency model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            race = Race.objects.get(index=row['races_index'])
            proficiency = Proficiency.objects.get(index=row['ref_index'])
            RaceStartingProficiency.objects.get_or_create(race=race, proficiency=proficiency)
    print("Races Starting Proficiencies loaded.")


def load_subraces_starting_proficiencies(file_path):
    """
    Load data from subraces_starting_proficiencies.csv into the SubraceStartingProficiency model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subrace = Subrace.objects.get(index=row['subraces_index'])
            proficiency = Proficiency.objects.get(index=row['ref_index'])
            SubraceStartingProficiency.objects.get_or_create(subrace=subrace, proficiency=proficiency)
    print("Subraces Starting Proficiencies loaded.")


def load_spell_classes(file_path):
    """
    Load data from spells_classes.csv into the SpellClass model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spell = Spell.objects.get(index=row['spells_index'])
            class_obj = Class.objects.get(index=row['ref_index'])
            SpellClass.objects.get_or_create(spell=spell, class_obj=class_obj)
    print("Spell Classes loaded.")


def load_spell_subclasses(file_path):
    """
    Load data from spells_subclasses.csv into the SpellSubclass model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spell = Spell.objects.get(index=row['spells_index'])
            subclass = Subclass.objects.get(index=row['ref_index'])
            SpellSubclass.objects.get_or_create(spell=spell, subclass=subclass)
    print("Spell Subclasses loaded.")


# Relationships Loaders
def load_classes_subclasses(file_path):
    """
    Load data from classes_subclasses.csv into the Subclass model.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_obj = Class.objects.get(index=row['classes_index'])
            subclass = Subclass.objects.get(index=row['ref_index'])

            # Ensure the subclass is properly linked to its class
            if subclass.class_obj != class_obj:
                subclass.class_obj = class_obj
                subclass.save()
    print("Classes-Subclasses relationships loaded.")


def load_races_subraces(file_path):
    """
    Load data from races_subraces.csv and ensure Subraces are correctly linked to their Races.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            race = Race.objects.get(index=row['races_index'])
            subrace = Subrace.objects.get(index=row['ref_index'])

            # Ensure the Subrace is linked to the correct Race
            if subrace.race != race:
                subrace.race = race
                subrace.save()
    print("Races-Subraces relationships loaded.")


if __name__ == "__main__":
    # Update paths to your CSV files
    base_dir = "csv_seed"
    load_classes(os.path.join(base_dir, 'classes.csv'))
    load_proficiencies(os.path.join(base_dir, 'proficiencies.csv'))
    load_races(os.path.join(base_dir, 'races.csv'))
    load_subraces(os.path.join(base_dir, 'subraces.csv'))
    load_subclasses(os.path.join(base_dir, 'subclasses.csv'))
    load_spells(os.path.join(base_dir, 'spells.csv'))
    load_class_proficiencies(os.path.join(base_dir, 'classes_proficiencies.csv'))
    load_proficiencies_classes(os.path.join(base_dir, 'proficiencies_classes.csv'))
    load_proficiencies_races(os.path.join(base_dir, 'proficiencies_races.csv'))
    load_races_starting_proficiencies(os.path.join(base_dir, 'races_starting_proficiencies.csv'))
    load_subraces_starting_proficiencies(os.path.join(base_dir, 'subraces_starting_proficiencies.csv'))
    load_subclasses_desc(os.path.join(base_dir, 'subclasses_desc.csv'))
    load_classes_subclasses(os.path.join(base_dir, 'classes_subclasses.csv'))
    load_races_subraces(os.path.join(base_dir, 'races_subraces.csv'))
    load_spell_descriptions(os.path.join(base_dir, 'spells_desc.csv'))
    load_spell_classes(os.path.join(base_dir, 'spells_classes.csv'))
    load_spell_subclasses(os.path.join(base_dir, 'spells_subclasses.csv'))
    print("All data loaded.")
