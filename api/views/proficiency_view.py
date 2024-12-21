from api.models import Proficiency
from api.serializers.proficiencies import ProficiencyListSerializer, ProficiencyDetailSerializer, \
    ProficiencyInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class ProficiencyViewSet(NoPutModelViewSet):
    """
    ViewSet for managing Proficiency objects.
    - List View: Uses ProficiencyListSerializer.
    - Detail View: Uses ProficiencyDetailSerializer.
    - Create/Update: Uses ProficiencyInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Proficiency.objects.all()

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the action.
        """
        if self.action == 'list':
            return ProficiencyListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProficiencyInputSerializer
        return ProficiencyDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Proficiency instance, handling relational links.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Proficiency instance, handling relational links.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Proficiency instance.
        """
        instance.delete()
