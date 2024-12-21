from rest_framework import serializers
from django.urls import reverse
from api.models import Race, Subrace, RaceStartingProficiency


# Serializer for listing races with basic details.
class RaceListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a field for the URL to the detailed view.

    class Meta:
        model = Race
        fields = ['id', 'index', 'name', 'detail_url']  # Exposes essential fields for race listings.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the race detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))


# Serializer for displaying detailed information about subraces.
class SubraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrace
        fields = ['id', 'index', 'name', 'desc']  # Exposes essential fields for subraces.


# Serializer for displaying starting proficiencies associated with a race.
class RaceStartingProficiencySerializer(serializers.ModelSerializer):
    proficiency_name = serializers.CharField(source="proficiency.name",
                                             read_only=True)  # Displays the name of the proficiency.
    proficiency_url = serializers.SerializerMethodField()  # Adds a field for the URL to the proficiency detail view.

    class Meta:
        model = RaceStartingProficiency
        fields = ['proficiency_name', 'proficiency_url']  # Exposes essential fields for starting proficiencies.

    def get_proficiency_url(self, obj):
        """
        Constructs and returns the absolute URL for the proficiency detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.proficiency.id]))


# Serializer for creating and updating races.
class RaceInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'  # Exposes all fields for create and update operations.


# Serializer for displaying detailed information about a race.
class RaceDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a field for the URL to the detailed view.
    subraces = SubraceSerializer(many=True, read_only=True)  # Displays associated subraces.
    starting_proficiencies = RaceStartingProficiencySerializer(many=True,
                                                               read_only=True)  # Displays associated starting proficiencies.

    class Meta:
        model = Race
        fields = '__all__'  # Exposes all fields, including nested relationships.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the race detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))
