from api.models import Subclass
from api.serializers.subclasses import SubclassListSerializer, SubclassDetailSerializer, SubclassInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class SubclassViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for Subclass instances.
    - List View: Uses SubclassListSerializer to return basic information about subclasses.
    - Detail View: Uses SubclassDetailSerializer to provide comprehensive details about a single subclass.
    - Create/Update: Uses SubclassInputSerializer to handle input for creating or updating subclasses.
    - Supports POST, PATCH, and DELETE actions (excludes PUT as per NoPutModelViewSet).
    """
    # QuerySet that retrieves all Subclass objects from the database.
    queryset = Subclass.objects.all()

    def get_serializer_class(self):
        """
        Determines and returns the appropriate serializer class based on the action being performed.
        - 'list': Uses SubclassListSerializer for summarized subclass data.
        - 'create', 'update', 'partial_update': Uses SubclassInputSerializer for handling input data.
        - Default: Uses SubclassDetailSerializer for detailed views.
        """
        if self.action == 'list':
            return SubclassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubclassInputSerializer
        return SubclassDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Subclass instance.
        - Saves the serialized data to create a new Subclass object in the database.
        - Allows for any additional pre-save logic if required in the future.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Subclass instance.
        - Saves the serialized data to update an existing Subclass object in the database.
        - Supports PATCH operations as full-object replacements (PUT) are excluded by design.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handles the deletion of a Subclass instance.
        - Deletes the specified Subclass object from the database.
        """
        instance.delete()
