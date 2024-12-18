from rest_framework import serializers
from django.urls import reverse
from api.models import Spell, SpellDescription, SpellClass, SpellSubclass


class SpellListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


class SpellDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellDescription
        fields = ['value']


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
    classes = SpellClassSerializer(many=True)
    subclasses = SpellSubclassSerializer(many=True)

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
