from rest_framework import serializers
from django.urls import reverse
from api.models import Race, Subrace, RaceStartingProficiency


# Serializer for displaying a list of races with basic details.
class RaceListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each race.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Race
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the race detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))


# Serializer for displaying detailed information about subraces.
class SubraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrace
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'desc']


# Serializer for displaying starting proficiencies associated with a race.
class RaceStartingProficiencySerializer(serializers.ModelSerializer):
    # Displays the name of the proficiency.
    proficiency_name = serializers.CharField(source="proficiency.name", read_only=True)
    # Provides the detail URL for the proficiency.
    proficiency_url = serializers.SerializerMethodField()

    class Meta:
        model = RaceStartingProficiency
        # Specifies the fields to include in the serialized output.
        fields = ['proficiency_name', 'proficiency_url']

    def get_proficiency_url(self, obj):
        """
        Returns the absolute URL for the proficiency detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.proficiency.id]))


# Serializer for displaying detailed information about a race, including related subraces and starting proficiencies.
class RaceDetailSerializer(serializers.ModelSerializer):
    # Provides the detail URL for the race.
    detail_url = serializers.SerializerMethodField()
    # Displays all subraces related to the race.
    subraces = SubraceSerializer(many=True)
    # Displays all starting proficiencies associated with the race.
    starting_proficiencies = RaceStartingProficiencySerializer(many=True)

    class Meta:
        model = Race
        # Specifies the fields to include in the serialized output.
        fields = [
            'id',  # Unique identifier of the race.
            'index',  # Index field for external referencing.
            'name',  # Name of the race.
            'age',  # Description of the race's age characteristics.
            'alignment',  # Typical alignment tendencies of the race.
            'language_desc',  # Description of the race's language capabilities.
            'size',  # Size category (e.g., Medium, Small).
            'size_description',  # Detailed physical size description.
            'speed',  # Base speed of the race.
            'subraces',  # List of related subraces.
            'starting_proficiencies',  # List of starting proficiencies.
            'detail_url',  # Detail URL for the race.
        ]

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the race detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))
