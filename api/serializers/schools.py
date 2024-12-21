from rest_framework import serializers
from api.models import School, Spell
from django.urls import reverse


# Serializer to list spells associated with a school.
class SpellListForSchoolSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each spell.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


# Serializer to display a list of schools with basic details.
class SchoolListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each school.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the school detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('school-detail', args=[obj.id]))


# Serializer to display detailed information about a school.
class SchoolDetailSerializer(serializers.ModelSerializer):
    # Lists all spells associated with the school.
    spells = SpellListForSchoolSerializer(many=True, read_only=True)  # Related spells using `related_name="spells"`

    class Meta:
        model = School
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'spells']
