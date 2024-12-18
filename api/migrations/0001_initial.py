# Generated by Django 5.1.4 on 2024-12-18 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('hit_die', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('age', models.TextField()),
                ('alignment', models.TextField()),
                ('language_desc', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=50)),
                ('size_description', models.TextField()),
                ('speed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ClassProficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_proficiencies', to='api.class')),
                ('proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_proficiencies', to='api.proficiency')),
            ],
        ),
        migrations.CreateModel(
            name='ProficiencyClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proficiency_classes', to='api.class')),
                ('proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proficiency_classes', to='api.proficiency')),
            ],
        ),
        migrations.CreateModel(
            name='RaceStartingProficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starting_races', to='api.proficiency')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starting_proficiencies', to='api.race')),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
                ('attack_type', models.CharField(blank=True, max_length=50, null=True)),
                ('casting_time', models.CharField(max_length=100)),
                ('concentration', models.BooleanField()),
                ('duration', models.CharField(max_length=100)),
                ('material', models.TextField(blank=True, null=True)),
                ('range', models.CharField(max_length=100)),
                ('ritual', models.BooleanField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='api.school')),
            ],
        ),
        migrations.CreateModel(
            name='SpellClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='api.class')),
                ('spell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='api.spell')),
            ],
        ),
        migrations.CreateModel(
            name='SpellDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('spell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descriptions', to='api.spell')),
            ],
        ),
        migrations.CreateModel(
            name='Subclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('subclass_flavor', models.CharField(max_length=100)),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subclasses', to='api.class')),
            ],
        ),
        migrations.CreateModel(
            name='SpellSubclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subclasses', to='api.spell')),
                ('subclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='api.subclass')),
            ],
        ),
        migrations.CreateModel(
            name='SubclassDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('subclass', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='description', to='api.subclass')),
            ],
        ),
        migrations.CreateModel(
            name='Subrace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=50, unique=True)),
                ('desc', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subraces', to='api.race')),
            ],
        ),
        migrations.CreateModel(
            name='ProficiencyRace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='races_and_subraces', to='api.proficiency')),
                ('race', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proficiencies', to='api.race')),
                ('subrace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proficiencies', to='api.subrace')),
            ],
        ),
        migrations.CreateModel(
            name='SubraceStartingProficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starting_subraces', to='api.proficiency')),
                ('subrace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='starting_proficiencies', to='api.subrace')),
            ],
        ),
    ]
