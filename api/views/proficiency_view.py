from api.models import Proficiency
from api.serializers.proficiencies import ProficiencyListSerializer, ProficiencyDetailSerializer, \
    ProficiencyInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class ProficiencyViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for Proficiency instances.
    - List View: Returns a summary of all proficiencies using ProficiencyListSerializer.
    - Detail View: Provides detailed information using ProficiencyDetailSerializer.
    - Create/Update: Supports input operations using ProficiencyInputSerializer.
    - Supports HTTP methods: POST, PATCH, and DELETE (no PUT).
    """
    queryset = Proficiency.objects.all()  # Retrieves all Proficiency objects for use in the ViewSet.

    def get_serializer_class(self):
        """
        Determines the appropriate serializer class based on the current action.
        - 'list': Uses ProficiencyListSerializer for summarized data.
        - 'create', 'update', 'partial_update': Uses ProficiencyInputSerializer for handling input data.
        - Default: Uses ProficiencyDetailSerializer for detailed views.
        """
        if self.action == 'list':
            return ProficiencyListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProficiencyInputSerializer
        return ProficiencyDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Proficiency instance.
        - Saves the instance using the provided serializer.
        - Handles any additional relational data if required.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Proficiency instance.
        - Updates the instance with the provided serializer.
        - Handles any additional logic for updating relational data if required.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Proficiency instance.
        - Deletes the instance and ensures any cascading deletions are handled.
        """
        instance.delete()
