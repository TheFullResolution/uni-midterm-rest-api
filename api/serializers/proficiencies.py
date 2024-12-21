from rest_framework import serializers
from django.urls import reverse
from api.models import Proficiency, ProficiencyClass, ProficiencyRace, Class


# Serializer for detailed information about a Proficiency (read-only).
class ProficiencyDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a URL field for the detail view of a proficiency.
    proficiency_classes = serializers.SerializerMethodField(read_only=True)  # Fetches related classes.
    races_and_subraces = serializers.SerializerMethodField(read_only=True)  # Fetches related races and subraces.

    class Meta:
        model = Proficiency
        fields = '__all__'  # Includes all fields of the Proficiency model in the serialized output.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the proficiency detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))

    def get_proficiency_classes(self, obj):
        """
        Retrieves all classes associated with this proficiency, including their names and detail URLs.
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
        Retrieves all races and subraces associated with this proficiency.
        Provides names and clickable URLs for detailed views.
        """
        request = self.context.get('request')
        races = obj.races_and_subraces.all()  # Leverages the related_name defined in the ProficiencyRace model.
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
    detail_url = serializers.SerializerMethodField()  # Adds a URL field for the proficiency detail view.

    class Meta:
        model = Proficiency
        fields = ['id', 'name', 'type', 'detail_url']  # Exposes essential fields for list views.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the proficiency detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


# Serializer for input operations on Proficiency, supporting relational data.
class ProficiencyInputSerializer(serializers.ModelSerializer):
    associated_classes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Class.objects.all(),  # Links to valid Class objects.
        required=False,
        source='proficiencyclass_set'  # Maps to the reverse relation for ProficiencyClass.
    )

    class Meta:
        model = Proficiency
        fields = '__all__'  # Includes all fields for input and relational mapping.

    def create(self, validated_data):
        """
        Creates a Proficiency instance and establishes relationships with Classes.
        """
        associated_classes = validated_data.pop('proficiencyclass_set', [])

        # Create the Proficiency instance with the provided data.
        proficiency_instance = Proficiency.objects.create(**validated_data)

        # Establish links to the associated classes.
        for class_obj in associated_classes:
            ProficiencyClass.objects.create(proficiency=proficiency_instance, class_obj=class_obj)

        return proficiency_instance

    def update(self, instance, validated_data):
        """
        Updates a Proficiency instance and manages relationships with Classes.
        """
        associated_classes = validated_data.pop('proficiencyclass_set', None)

        if associated_classes is not None:
            # Clear existing links and re-establish relationships.
            ProficiencyClass.objects.filter(proficiency=instance).delete()
            for class_obj in associated_classes:
                ProficiencyClass.objects.create(proficiency=instance, class_obj=class_obj)

        return super().update(instance, validated_data)


# Serializer for associating a proficiency with a class.
class ProficiencyClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_obj.name", read_only=True)  # Displays the class name.
    detail_url = serializers.SerializerMethodField()  # Adds a URL field for the class detail view.

    class Meta:
        model = ProficiencyClass
        fields = ['class_name', 'detail_url']  # Exposes relevant fields for this association.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the class detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for associating a proficiency with a race and subrace.
class ProficiencyRaceSerializer(serializers.ModelSerializer):
    race_name = serializers.CharField(source="race.name", read_only=True)  # Displays the race name.
    subrace_name = serializers.CharField(source="subrace.name", read_only=True)  # Displays the subrace name.

    class Meta:
        model = ProficiencyRace
        fields = ['race_name', 'subrace_name']  # Exposes relevant fields for this association.


# Serializer for the Proficiency model, representing detailed information.
class ProficiencySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a URL field for the proficiency detail view.

    class Meta:
        model = Proficiency
        fields = '__all__'  # Includes all fields of the Proficiency model.
        depth = 2  # Adds nested serialization for related objects.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the proficiency detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))
