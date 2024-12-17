from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Class, Proficiency, Race, Spell, School
from .serializers import ProficiencySerializer, RaceSerializer, SpellSerializer, SchoolSerializer, ClassListSerializer, \
    ClassDetailSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ClassListSerializer  # Minimal serializer for list view
        return ClassDetailSerializer  # Detailed serializer for retrieve view


class ProficiencyViewSet(viewsets.ModelViewSet):
    queryset = Proficiency.objects.all()
    serializer_class = ProficiencySerializer
    permission_classes = [AllowAny]


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    permission_classes = [AllowAny]


class SpellViewSet(viewsets.ModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer
    permission_classes = [AllowAny]


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [AllowAny]
