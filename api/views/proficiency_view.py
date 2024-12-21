from api.models import Proficiency
from api.serializers import ProficiencyListSerializer, ProficiencyDetailSerializer, ProficiencyInputSerializer
from .base_viewsets import NoPutModelViewSet


class ProficiencyViewSet(NoPutModelViewSet):
    """
    ViewSet for managing Proficiencies.
    - List View: Uses ProficiencyListSerializer.
    - Detail View: Uses ProficiencyDetailSerializer.
    - Create/Update: Uses ProficiencyInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Proficiency.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProficiencyListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProficiencyInputSerializer
        return ProficiencyDetailSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
