from rest_framework import serializers, viewsets
from django.urls import reverse

from api.models import Class, SpellClass, ClassProficiency
from api.serializers.proficiencies import ProficiencyListSerializer


# Serializer for handling the relationship between a class and its spells (read-only).
class ClassSpellSerializer(serializers.ModelSerializer):
    spell_name = serializers.CharField(source="spell.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = ['id', 'spell_name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.spell.id]))


# Serializer for listing classes with basic details (read-only).
class ClassListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))


# Serializer for creating or updating classes (input serializer).
class ClassInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'  # Allow all fields for create and update


# Serializer for displaying detailed information about a class (read-only).
class ClassDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class_proficiencies = serializers.SerializerMethodField(read_only=True)
    spells = ClassSpellSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = '__all__'

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))

    def get_class_proficiencies(self, obj):
        proficiencies = ClassProficiency.objects.filter(class_obj=obj)
        return ProficiencyListSerializer([p.proficiency for p in proficiencies], many=True, context=self.context).data


# ViewSet to manage Class objects, enabling POST, PATCH, and DELETE actions.
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the action.
        """
        if self.action == 'list':
            return ClassListSerializer  # For GET (list)
        elif self.action in ['create', 'partial_update', 'update']:
            return ClassInputSerializer  # For POST and PATCH
        return ClassDetailSerializer  # For GET (detail)

    def perform_create(self, serializer):
        """
        Custom logic during object creation (POST).
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic during object update (PATCH or PUT).
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic during object deletion (DELETE).
        """
        instance.delete()
