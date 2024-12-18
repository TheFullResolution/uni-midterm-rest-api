from rest_framework import serializers
from django.urls import reverse
from .models import Class, Proficiency, Race, Spell, School, ClassProficiency, SpellClass, SubclassDescription, \
    Subclass, ProficiencyClass, ProficiencyRace, Subrace, RaceStartingProficiency, SpellSubclass, SpellDescription


class ClassSpellSerializer(serializers.ModelSerializer):
    spell_name = serializers.CharField(source="spell.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = ['id', 'spell_name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')  # Get the request context
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.spell.id]))


# Subclass Description Serializer
class SubclassDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubclassDescription
        fields = ['value']


# Subclass Serializer
class SubclassSerializer(serializers.ModelSerializer):
    description = SubclassDescriptionSerializer()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Subclass
        fields = ['id', 'index', 'name', 'subclass_flavor', 'description', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')  # Get the request context
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))


class ClassListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'detail_url']  # Minimal fields for the list view

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))


class ClassDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class_proficiencies = serializers.SerializerMethodField()
    spells = ClassSpellSerializer(many=True)
    subclasses = SubclassSerializer(many=True)

    class Meta:
        model = Class
        fields = ['id', 'index', 'hit_die', 'name', 'class_proficiencies', 'spells', 'subclasses', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))

    def get_class_proficiencies(self, obj):
        proficiencies = ClassProficiency.objects.filter(class_obj=obj)
        return ProficiencySerializer([p.proficiency for p in proficiencies], many=True, context=self.context).data


class ProficiencySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        fields = '__all__'
        depth = 2

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


class ProficiencyClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = ProficiencyClass
        fields = ['class_name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')  # Get the request context
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for related Race and Subrace (used in ProficiencyDetailSerializer)
class ProficiencyRaceSerializer(serializers.ModelSerializer):
    race_name = serializers.CharField(source="race.name", read_only=True)
    subrace_name = serializers.CharField(source="subrace.name", read_only=True)

    class Meta:
        model = ProficiencyRace
        fields = ['race_name', 'subrace_name']


# Minimal Proficiency List Serializer
class ProficiencyListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        fields = ['id', 'name', 'type', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


# Detailed Proficiency Serializer
class ProficiencyDetailSerializer(serializers.ModelSerializer):
    proficiency_classes = ProficiencyClassSerializer(many=True)
    races_and_subraces = ProficiencyRaceSerializer(many=True)

    class Meta:
        model = Proficiency
        fields = ['id', 'index', 'name', 'type', 'proficiency_classes', 'races_and_subraces']


class RaceListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields = ['id', 'index', 'name', 'detail_url']  # Minimal fields for the list view

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))


class SubraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrace
        fields = ['id', 'index', 'name', 'desc']  # Include subrace fields as needed


class RaceStartingProficiencySerializer(serializers.ModelSerializer):
    proficiency_name = serializers.CharField(source="proficiency.name", read_only=True)
    proficiency_url = serializers.SerializerMethodField()

    class Meta:
        model = RaceStartingProficiency
        fields = ['proficiency_name', 'proficiency_url']

    def get_proficiency_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.proficiency.id]))


class RaceDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    subraces = SubraceSerializer(many=True)  # Use related_name "subraces"
    starting_proficiencies = RaceStartingProficiencySerializer(many=True)  # Use related_name "starting_proficiencies"

    class Meta:
        model = Race
        fields = [
            'id',
            'index',
            'name',
            'age',
            'alignment',
            'language_desc',
            'size',
            'size_description',
            'speed',
            'subraces',
            'starting_proficiencies',
            'detail_url',
        ]

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))


class SpellListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ['id', 'index', 'name', 'detail_url']  # Minimal fields for the list view

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


class SpellDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellDescription
        fields = ['value']  # Include the description text


class SpellClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    class_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = ['class_name', 'class_url']

    def get_class_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


class SpellSubclassSerializer(serializers.ModelSerializer):
    subclass_name = serializers.CharField(source="subclass.name", read_only=True)
    subclass_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellSubclass
        fields = ['subclass_name', 'subclass_url']

    def get_subclass_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.subclass.id]))


class SpellDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    school_name = serializers.CharField(source="school.name", read_only=True)
    descriptions = SpellDescriptionSerializer(many=True)
    classes = SpellClassSerializer(many=True)  # Use related_name "classes"
    subclasses = SpellSubclassSerializer(many=True)  # Use related_name "subclasses"

    class Meta:
        model = Spell
        fields = [
            'id',
            'index',
            'name',
            'level',
            'attack_type',
            'casting_time',
            'concentration',
            'duration',
            'material',
            'range',
            'ritual',
            'school_name',
            'descriptions',
            'classes',
            'subclasses',
            'detail_url',
        ]

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


class SpellListForSchoolSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


class SchoolDetailSerializer(serializers.ModelSerializer):
    spells = SpellListForSchoolSerializer(many=True, read_only=True)  # Related spells using the `related_name="spells"`

    class Meta:
        model = School
        fields = ['id', 'index', 'name', 'spells']
