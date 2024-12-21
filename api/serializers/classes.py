from rest_framework import serializers
from django.urls import reverse

from api.models import Class, SpellClass, ClassProficiency
from api.serializers.proficiencies import ProficiencySerializer


# Serializer to represent the relationship between a class and its spells.
class ClassSpellSerializer(serializers.ModelSerializer):
    # Displays the name of the associated spell.
    spell_name = serializers.CharField(source="spell.name", read_only=True)
    # Provides the detail URL for the spell.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'spell_name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.spell.id]))


# Serializer for displaying a list of classes with basic details.
class ClassListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for the class.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the class detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))


# Serializer for displaying detailed information about a specific class.
class ClassDetailSerializer(serializers.ModelSerializer):
    # Provides the detail URL for the class.
    detail_url = serializers.SerializerMethodField()
    # Displays the list of proficiencies associated with the class.
    class_proficiencies = serializers.SerializerMethodField()
    # Displays the list of spells associated with the class.
    spells = ClassSpellSerializer(many=True)

    class Meta:
        model = Class
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'hit_die', 'name', 'class_proficiencies', 'spells', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the class detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))

    def get_class_proficiencies(self, obj):
        """
        Retrieves and serializes the list of proficiencies associated with the given class.
        Proficiency data is serialized using the ProficiencySerializer.
        """
        proficiencies = ClassProficiency.objects.filter(class_obj=obj)  # Query for related proficiencies.
        # Serialize and return the proficiency data.
        return ProficiencySerializer([p.proficiency for p in proficiencies], many=True, context=self.context).data
