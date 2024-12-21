from rest_framework import serializers
from django.urls import reverse
from api.models import Proficiency, ProficiencyClass, ProficiencyRace


# Serializer for the Proficiency model, representing detailed information about a proficiency.
class ProficiencySerializer(serializers.ModelSerializer):
    # Provides the detail URL for the proficiency.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        # Includes all fields from the model and sets depth for nested serialization.
        fields = '__all__'
        depth = 2

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the proficiency detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


# Serializer for associating a proficiency with a class.
class ProficiencyClassSerializer(serializers.ModelSerializer):
    # Displays the name of the associated class.
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    # Provides the detail URL for the class.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = ProficiencyClass
        # Specifies the fields to include in the serialized output.
        fields = ['class_name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the class detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Get the request context.
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for associating a proficiency with a race and subrace.
class ProficiencyRaceSerializer(serializers.ModelSerializer):
    # Displays the name of the associated race.
    race_name = serializers.CharField(source="race.name", read_only=True)
    # Displays the name of the associated subrace.
    subrace_name = serializers.CharField(source="subrace.name", read_only=True)

    class Meta:
        model = ProficiencyRace
        # Specifies the fields to include in the serialized output.
        fields = ['race_name', 'subrace_name']


# Serializer for listing proficiencies with minimal details.
class ProficiencyListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for the proficiency.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'name', 'type', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the proficiency detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


# Serializer for providing detailed information about a proficiency.
class ProficiencyDetailSerializer(serializers.ModelSerializer):
    # Lists all classes associated with the proficiency.
    proficiency_classes = ProficiencyClassSerializer(many=True)
    # Lists all races and subraces associated with the proficiency.
    races_and_subraces = ProficiencyRaceSerializer(many=True)

    class Meta:
        model = Proficiency
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'type', 'proficiency_classes', 'races_and_subraces']
