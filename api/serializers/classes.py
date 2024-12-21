from django.urls import reverse
from rest_framework import serializers
from api.models import Class, ClassProficiency, Proficiency, SpellClass


# Serializer for linking spells to their associated classes.
class ClassSpellSerializer(serializers.ModelSerializer):
    # Displays the name of the spell associated with the class.
    spell_name = serializers.CharField(source="spell.name", read_only=True)
    # Provides the URL to the spell's detail view.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = ['id', 'spell_name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the related spell detail view.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.spell.id]))


# Serializer for linking proficiencies to their associated classes.
class ClassProficiencySerializer(serializers.ModelSerializer):
    # Displays the name of the proficiency associated with the class.
    proficiency_name = serializers.CharField(source="proficiency.name", read_only=True)
    # Provides the URL to the proficiency's detail view.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = ClassProficiency
        fields = ['id', 'proficiency_name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the related proficiency detail view.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.proficiency.id]))


# Serializer for listing class information with links to detailed views.
class ClassListSerializer(serializers.ModelSerializer):
    # Provides the URL to the class's detail view.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the class detail view.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))


# Serializer for handling class input, including associated proficiencies.
class ClassInputSerializer(serializers.ModelSerializer):
    # Allows linking multiple proficiencies by their primary keys.
    proficiencies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Proficiency.objects.all(),
        required=False,
    )

    class Meta:
        model = Class
        fields = ['id', 'index', 'hit_die', 'name', 'proficiencies']

    def create(self, validated_data):
        """
        Creates a new Class instance along with its associated proficiencies.
        """
        proficiencies = validated_data.pop('proficiencies', [])
        class_instance = Class.objects.create(**validated_data)
        for proficiency in proficiencies:
            ClassProficiency.objects.create(class_obj=class_instance, proficiency=proficiency)
        return class_instance

    def update(self, instance, validated_data):
        """
        Updates an existing Class instance and its associated proficiencies.
        """
        proficiencies = validated_data.pop('proficiencies', None)
        if proficiencies is not None:
            # Clear existing proficiencies before adding new ones.
            instance.class_proficiencies.all().delete()
            for proficiency in proficiencies:
                ClassProficiency.objects.create(class_obj=instance, proficiency=proficiency)
        return super().update(instance, validated_data)


# Serializer for providing detailed class information, including related entities.
class ClassDetailSerializer(serializers.ModelSerializer):
    # Provides the URL to the class's detail view.
    detail_url = serializers.SerializerMethodField()
    # Includes detailed information about the class's proficiencies.
    class_proficiencies = ClassProficiencySerializer(many=True, read_only=True)
    # Provides a simplified representation of associated subclasses.
    subclasses = serializers.SerializerMethodField()
    # Includes detailed information about the spells associated with the class.
    spells = ClassSpellSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'index', 'hit_die', 'name', 'detail_url', 'class_proficiencies', 'subclasses', 'spells']

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the class detail view.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))

    def get_subclasses(self, obj):
        """
        Constructs and returns a list of simplified subclass representations,
        including their URLs, IDs, and names.
        """
        request = self.context.get('request')
        return [
            {
                "url": request.build_absolute_uri(reverse('subclass-detail', args=[subclass.id])),
                "id": subclass.id,
                "name": subclass.name,
            }
            for subclass in obj.subclasses.all()
        ]
