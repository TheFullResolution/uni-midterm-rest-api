from api.models import Class
from api.serializers import (
    ClassListSerializer,
    ClassDetailSerializer,
    ClassInputSerializer
)
from .base_viewsets import NoPutModelViewSet


class ClassViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for Class instances.
    - List View: Returns a summary of all classes using ClassListSerializer.
    - Detail View: Provides detailed information using ClassDetailSerializer.
    - Create/Update: Supports input operations using ClassInputSerializer.
    - Supports HTTP methods: POST, PATCH, and DELETE (no PUT).
    """
    queryset = Class.objects.prefetch_related(
        'class_proficiencies__proficiency',
        'subclasses',
        'spells'
    ).all()

    def get_serializer_class(self):
        """
        Determines the appropriate serializer class based on the current action.
        - 'list': Uses ClassListSerializer for summarized data.
        - 'create', 'update', 'partial_update': Uses ClassInputSerializer for handling input data.
        - Default: Uses ClassDetailSerializer for detailed views.
        """
        if self.action == 'list':
            return ClassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClassInputSerializer
        return ClassDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Class instance.
        - Saves the instance using the provided serializer.
        - Handles any additional relational data if required.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Class instance.
        - Updates the instance with the provided serializer.
        - Handles any additional logic for updating relational data if required.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Class instance.
        - Deletes the instance and ensures any cascading deletions are handled.
        """
        instance.delete()
