from rest_framework import serializers
from django.urls import reverse
from api.models import Proficiency, ProficiencyClass, ProficiencyRace, Class


# Serializer for detailed information about a Proficiency (read-only).
class ProficiencyDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    proficiency_classes = serializers.SerializerMethodField(read_only=True)
    races_and_subraces = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Proficiency
        fields = '__all__'

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the proficiency detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))

    def get_proficiency_classes(self, obj):
        """
        Retrieve all classes associated with this proficiency.
        """
        classes = ProficiencyClass.objects.filter(proficiency=obj)
        return [
            {
                'class_name': c.class_obj.name,
                'class_url': reverse('class-detail', args=[c.class_obj.id])
            }
            for c in classes
        ]

    def get_races_and_subraces(self, obj):
        """
        Retrieve all races and subraces associated with this proficiency,
        including clickable detail URLs using consistent logic.
        """
        request = self.context.get('request')  # Access the current request context
        races = obj.races_and_subraces.all()  # Uses the related_name from the ProficiencyRace model
        return [
            {
                'race_name': r.race.name if r.race else "Unknown",
                'subrace_name': r.subrace.name if r.subrace else "None",
                'race_detail_url': request.build_absolute_uri(
                    reverse('race-detail', args=[r.race.id])) if r.race else None,
                'subrace_detail_url': request.build_absolute_uri(
                    reverse('subrace-detail', args=[r.subrace.id])) if r.subrace else None,
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
        """
        Returns the absolute URL for the proficiency detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


class ProficiencyInputSerializer(serializers.ModelSerializer):
    associated_classes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Class.objects.all(),  # Correct queryset for Class objects
        required=False,
        source='proficiencyclass_set'  # Map to the reverse relation
    )

    class Meta:
        model = Proficiency
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a Proficiency instance and establish relationships with Classes.
        """
        associated_classes = validated_data.pop('proficiencyclass_set', [])

        proficiency_instance = Proficiency.objects.create(**validated_data)

        for class_obj in associated_classes:
            ProficiencyClass.objects.create(proficiency=proficiency_instance, class_obj=class_obj)

        return proficiency_instance

    def update(self, instance, validated_data):
        """
        Update a Proficiency instance and handle its relationships.
        """
        associated_classes = validated_data.pop('proficiencyclass_set', None)

        if associated_classes is not None:
            # Clear existing relationships before adding new ones
            ProficiencyClass.objects.filter(proficiency=instance).delete()
            for class_obj in associated_classes:
                # Add error handling for invalid Class objects
                ProficiencyClass.objects.create(proficiency=instance, class_obj=class_obj)

        return super().update(instance, validated_data)


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
