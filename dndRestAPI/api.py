from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Class, Proficiency, Race, Spell, School, Subclass
from .serializers import ClassListSerializer, \
    ClassDetailSerializer, ProficiencyListSerializer, ProficiencyDetailSerializer, SubclassSerializer, \
    RaceListSerializer, RaceDetailSerializer, SpellListSerializer, SpellDetailSerializer, SchoolDetailSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ClassListSerializer  # Minimal serializer for list view
        return ClassDetailSerializer  # Detailed serializer for retrieve view


class ProficiencyViewSet(viewsets.ModelViewSet):
    queryset = Proficiency.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProficiencyListSerializer  # Minimal serializer for list view
        return ProficiencyDetailSerializer  # Detailed serializer for retrieve view


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RaceListSerializer  # Minimal serializer for list view
        return RaceDetailSerializer  # Detailed serializer for retrieve view


class SpellViewSet(viewsets.ModelViewSet):
    queryset = Spell.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SpellListSerializer  # Minimal serializer for list view
        return SpellDetailSerializer  # Detailed serializer for retrieve view


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializer
    permission_classes = [AllowAny]


class SubclassViewSet(viewsets.ModelViewSet):
    queryset = Subclass.objects.all()
    serializer_class = SubclassSerializer
    permission_classes = [AllowAny]
