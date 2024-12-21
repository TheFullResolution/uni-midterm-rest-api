from rest_framework import serializers
from django.urls import reverse
from api.models import Spell, SpellDescription, SpellClass, SpellSubclass


# Serializer for listing spells with minimal details.
class SpellListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a field for the detail URL of the spell.

    class Meta:
        model = Spell
        fields = ['id', 'index', 'name', 'detail_url']  # Exposes essential fields for spell listings.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the spell detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


# Serializer for displaying detailed descriptions associated with spells.
class SpellDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellDescription
        fields = '__all__'  # Includes all fields from the SpellDescription model.


# Serializer for associating a spell with a class.
class SpellClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_obj.name", read_only=True)  # Displays the class name.
    class_url = serializers.SerializerMethodField()  # Adds a field for the class detail URL.

    class Meta:
        model = SpellClass
        fields = '__all__'  # Includes all fields from the SpellClass model.

    def get_class_url(self, obj):
        """
        Constructs and returns the absolute URL for the class detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for associating a spell with a subclass.
class SpellSubclassSerializer(serializers.ModelSerializer):
    subclass_name = serializers.CharField(source="subclass.name", read_only=True)  # Displays the subclass name.
    subclass_url = serializers.SerializerMethodField()  # Adds a field for the subclass detail URL.

    class Meta:
        model = SpellSubclass
        fields = '__all__'  # Includes all fields from the SpellSubclass model.

    def get_subclass_url(self, obj):
        """
        Constructs and returns the absolute URL for the subclass detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.subclass.id]))


# Serializer for creating and updating spells.
class SpellInputSerializer(serializers.ModelSerializer):
    """
    Handles the serialization and validation of input data for creating or updating spells.
    """

    class Meta:
        model = Spell
        fields = '__all__'  # Includes all fields for input operations.


# Serializer for displaying detailed information about a spell.
class SpellDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a field for the spell detail URL.
    school_name = serializers.CharField(source="school.name", read_only=True)  # Displays the school name.
    descriptions = SpellDescriptionSerializer(many=True)  # Includes nested spell descriptions.
    classes = SpellClassSerializer(many=True)  # Includes nested spell-class relationships.
    subclasses = SpellSubclassSerializer(many=True)  # Includes nested spell-subclass relationships.

    class Meta:
        model = Spell
        fields = '__all__'  # Exposes all fields with nested relationships for detailed views.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the spell detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))
