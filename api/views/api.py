from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.models import Class, Proficiency, Race, Spell, School, Subclass
from api.serializers import ClassListSerializer, \
    ClassDetailSerializer, ProficiencyListSerializer, ProficiencyDetailSerializer, \
    RaceListSerializer, RaceDetailSerializer, SpellListSerializer, SpellDetailSerializer, SchoolDetailSerializer, \
    SubclassListSerializer, SubclassDetailSerializer
from api.serializers.schools import SchoolListSerializer


# ViewSet for managing Class objects
class ClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Class data.
    - List View: Displays basic details using ClassListSerializer.
    - Detail View: Displays detailed information using ClassDetailSerializer.
    """
    queryset = Class.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the action ('list' or 'retrieve').
        """
        if self.action == 'list':
            return ClassListSerializer  # Minimal serializer for list view
        return ClassDetailSerializer  # Detailed serializer for retrieve view


# ViewSet for managing Proficiency objects
class ProficiencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Proficiency data.
    - List View: Displays basic details using ProficiencyListSerializer.
    - Detail View: Displays detailed information using ProficiencyDetailSerializer.
    """
    queryset = Proficiency.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the action ('list' or 'retrieve').
        """
        if self.action == 'list':
            return ProficiencyListSerializer  # Minimal serializer for list view
        return ProficiencyDetailSerializer  # Detailed serializer for retrieve view


# ViewSet for managing Race objects
class RaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Race data.
    - List View: Displays basic details using RaceListSerializer.
    - Detail View: Displays detailed information using RaceDetailSerializer.
    """
    queryset = Race.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the action ('list' or 'retrieve').
        """
        if self.action == 'list':
            return RaceListSerializer  # Minimal serializer for list view
        return RaceDetailSerializer  # Detailed serializer for retrieve view


# ViewSet for managing Spell objects
class SpellViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Spell data.
    - List View: Displays basic details using SpellListSerializer.
    - Detail View: Displays detailed information using SpellDetailSerializer.
    """
    queryset = Spell.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the action ('list' or 'retrieve').
        """
        if self.action == 'list':
            return SpellListSerializer  # Minimal serializer for list view
        return SpellDetailSerializer  # Detailed serializer for retrieve view


# ViewSet for managing School objects
class SchoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling School data.
    - List View: Displays basic details using SchoolListSerializer.
    - Detail View: Displays detailed information using SchoolDetailSerializer.
    """
    queryset = School.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the action ('list' or 'retrieve').
        """
        if self.action == 'list':
            return SchoolListSerializer  # Minimal serializer for list view
        return SchoolDetailSerializer  # Detailed serializer for retrieve view


# ViewSet for managing Subclass objects
class SubclassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Subclass data.
    - List View: Displays id, index, name, and detail_url using SubclassListSerializer.
    - Detail View: Displays all Subclass information including the linked Class and its detail_url using SubclassDetailSerializer.
    """
    queryset = Subclass.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the action ('list' or 'retrieve').
        """
        if self.action == 'list':
            return SubclassListSerializer
        return SubclassDetailSerializer

    def get_queryset(self):
        """
        Customizes the queryset to prefetch related data for optimization.
        Prefetches the linked Class object for efficiency.
        """
        return super().get_queryset().select_related('class_obj')
