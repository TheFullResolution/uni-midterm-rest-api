from rest_framework import serializers
from django.urls import reverse
from api.models import Spell, SpellDescription, SpellClass, SpellSubclass


# Serializer to list spells with basic information.
class SpellListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ['id', 'index', 'name', 'detail_url']  # Minimal fields for listing

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


# Serializer for displaying detailed descriptions of spells.
class SpellDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellDescription
        fields = '__all__'  # Include all fields from SpellDescription


# Serializer for associating a spell with a class.
class SpellClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    class_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = '__all__'  # Include all fields for SpellClass with additional logic for custom fields

    def get_class_url(self, obj):
        """
        Returns the absolute URL for the class detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for associating a spell with a subclass.
class SpellSubclassSerializer(serializers.ModelSerializer):
    subclass_name = serializers.CharField(source="subclass.name", read_only=True)
    subclass_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellSubclass
        fields = '__all__'  # Include all fields for SpellSubclass with additional logic for custom fields

    def get_subclass_url(self, obj):
        """
        Returns the absolute URL for the subclass detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.subclass.id]))


# Serializer for creating and updating spells (input serializer).
class SpellInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = '__all__'  # Allow all fields for create and update


# Serializer for displaying detailed information about a spell (read-only).
class SpellDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    school_name = serializers.CharField(source="school.name", read_only=True)
    descriptions = SpellDescriptionSerializer(many=True)
    classes = SpellClassSerializer(many=True)
    subclasses = SpellSubclassSerializer(many=True)

    class Meta:
        model = Spell
        fields = '__all__'  # Include all fields with additional logic for nested relationships

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))
