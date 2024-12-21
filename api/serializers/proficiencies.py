from rest_framework import serializers
from django.urls import reverse
from api.models import Proficiency, ProficiencyClass, ProficiencyRace


# Serializer for detailed information about a Proficiency (read-only).
class ProficiencyDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    proficiency_classes = serializers.SerializerMethodField(read_only=True)
    races_and_subraces = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Proficiency
        fields = '__all__'

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))

    def get_proficiency_classes(self, obj):
        """
        Retrieve all classes associated with this proficiency.
        """
        classes = ProficiencyClass.objects.filter(proficiency=obj)
        return [{'class_name': c.class_obj.name, 'class_url': reverse('class-detail', args=[c.class_obj.id])} for c in
                classes]

    def get_races_and_subraces(self, obj):
        """
        Retrieve all races and subraces associated with this proficiency.
        """
        races = ProficiencyRace.objects.filter(proficiency=obj)
        return [
            {
                'race_name': r.race.name,
                'subrace_name': r.subrace.name if r.subrace else None,
                'race_url': reverse('race-detail', args=[r.race.id])
            }
            for r in races
        ]


# Serializer for listing Proficiencies with minimal details (read-only).
class ProficiencyListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        fields = ['id', 'name', 'type', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


# Serializer for creating and updating Proficiencies.
class ProficiencyInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proficiency
        fields = '__all__'  # Allow all fields for create and update


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
