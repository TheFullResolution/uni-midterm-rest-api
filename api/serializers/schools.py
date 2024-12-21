from rest_framework import serializers
from api.models import School, Spell
from django.urls import reverse


# Serializer to list spells associated with a school.
class SpellListForSchoolSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each spell.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the spell detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


# Serializer to display a list of schools with basic details (read-only).
class SchoolListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each school.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the school detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('school-detail', args=[obj.id]))


# Serializer for creating and updating schools (input serializer).
class SchoolInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'  # Allow all fields for create and update


# Serializer to display detailed information about a school (read-only).
class SchoolDetailSerializer(serializers.ModelSerializer):
    # Lists all spells associated with the school.
    spells = SpellListForSchoolSerializer(many=True, read_only=True)  # Related spells using `related_name="spells"`

    class Meta:
        model = School
        fields = '__all__'  # Allow all fields for create and update
