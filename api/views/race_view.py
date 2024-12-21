from api.models import Race
from api.serializers import RaceListSerializer, RaceDetailSerializer, RaceInputSerializer
from .base_viewsets import NoPutModelViewSet


class RaceViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for Race instances.
    - List View: Returns a summarized view of races using RaceListSerializer.
    - Detail View: Provides detailed information using RaceDetailSerializer.
    - Create/Update: Handles input for creating or updating races using RaceInputSerializer.
    - Supports POST, PATCH, and DELETE actions (No PUT method allowed as per project design).
    """
    # Retrieves all Race objects from the database.
    queryset = Race.objects.all()

    def get_serializer_class(self):
        """
        Determines which serializer to use based on the action being performed:
        - 'list': Returns basic details for each race using RaceListSerializer.
        - 'create', 'update', 'partial_update': Handles input and validation using RaceInputSerializer.
        - Default: Returns detailed race information using RaceDetailSerializer.
        """
        if self.action == 'list':
            return RaceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RaceInputSerializer
        return RaceDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Race instance.
        - Uses the provided serializer to save the instance to the database.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Race instance.
        - Uses the provided serializer to update the instance in the database.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handles the deletion of a Race instance.
        - Deletes the instance from the database.
        """
        instance.delete()
