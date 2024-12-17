from rest_framework import serializers
from django.urls import reverse
from .models import Class, Proficiency, Race, Spell, School, ClassProficiency, SpellClass, SubclassDescription, Subclass


# Spell Serializer
class SpellClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellClass
        fields = ['spell']


# Subclass Description Serializer
class SubclassDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubclassDescription
        fields = ['value']


# Subclass Serializer
class SubclassSerializer(serializers.ModelSerializer):
    description = SubclassDescriptionSerializer()

    class Meta:
        model = Subclass
        fields = ['index', 'name', 'subclass_flavor', 'description']


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
    spells = SpellClassSerializer(many=True)
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


class RaceSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields = '__all__'
        depth = 2

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))


class SpellSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = '__all__'
        depth = 2

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


class SchoolSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = '__all__'
        depth = 2

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('school-detail', args=[obj.id]))
