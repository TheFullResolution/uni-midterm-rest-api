from rest_framework import serializers
from django.urls import reverse
from api.models import Spell, SpellDescription, SpellClass, SpellSubclass


# Serializer to list spells with basic information.
class SpellListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each spell.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


# Serializer for displaying detailed descriptions of spells.
class SpellDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellDescription
        # Includes the 'value' field, which contains the detailed description of the spell.
        fields = ['value']


# Serializer for associating a spell with a class.
class SpellClassSerializer(serializers.ModelSerializer):
    # Displays the name of the associated class.
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    # Provides the detail URL for the associated class.
    class_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        # Specifies the fields to include in the serialized output.
        fields = ['class_name', 'class_url']

    def get_class_url(self, obj):
        """
        Returns the absolute URL for the class detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for associating a spell with a subclass.
class SpellSubclassSerializer(serializers.ModelSerializer):
    # Displays the name of the associated subclass.
    subclass_name = serializers.CharField(source="subclass.name", read_only=True)
    # Provides the detail URL for the associated subclass.
    subclass_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellSubclass
        # Specifies the fields to include in the serialized output.
        fields = ['subclass_name', 'subclass_url']

    def get_subclass_url(self, obj):
        """
        Returns the absolute URL for the subclass detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.subclass.id]))


# Serializer for displaying detailed information about a spell.
class SpellDetailSerializer(serializers.ModelSerializer):
    # Provides the detail URL for the spell.
    detail_url = serializers.SerializerMethodField()
    # Displays the name of the associated school of magic.
    school_name = serializers.CharField(source="school.name", read_only=True)
    # Displays a list of detailed descriptions of the spell.
    descriptions = SpellDescriptionSerializer(many=True)
    # Displays the classes associated with the spell.
    classes = SpellClassSerializer(many=True)
    # Displays the subclasses associated with the spell.
    subclasses = SpellSubclassSerializer(many=True)

    class Meta:
        model = Spell
        # Specifies the fields to include in the serialized output.
        fields = [
            'id',  # Unique identifier of the spell.
            'index',  # Index field for external referencing.
            'name',  # Name of the spell.
            'level',  # Level of the spell, indicating its complexity.
            'attack_type',  # Type of attack the spell involves (if applicable).
            'casting_time',  # Time required to cast the spell.
            'concentration',  # Whether the spell requires concentration.
            'duration',  # Duration of the spell's effects.
            'material',  # Material components needed for the spell.
            'range',  # Effective range of the spell.
            'ritual',  # Whether the spell can be cast as a ritual.
            'school_name',  # Name of the associated school of magic.
            'descriptions',  # Detailed descriptions of the spell.
            'classes',  # Classes associated with the spell.
            'subclasses',  # Subclasses associated with the spell.
            'detail_url',  # Detail URL for the spell.
        ]

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))
