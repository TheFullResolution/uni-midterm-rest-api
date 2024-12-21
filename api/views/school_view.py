from api.models import School
from api.serializers.schools import SchoolListSerializer, SchoolDetailSerializer, SchoolInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class SchoolViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for School instances.
    - Inherits from NoPutModelViewSet, which excludes the PUT method to ensure partial updates
      (PATCH) are used instead of full replacements.
    - List View: Uses SchoolListSerializer to display basic information.
    - Detail View: Uses SchoolDetailSerializer to display detailed information.
    - Create/Update: Uses SchoolInputSerializer to handle input for creating or updating School instances.
    - Supports POST, PATCH, and DELETE actions, providing CRUD functionality.
    """
    queryset = School.objects.all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer class based on the current action.
        - 'list': Returns summarized data using SchoolListSerializer.
        - 'create', 'update', 'partial_update': Uses SchoolInputSerializer for input operations.
        - Default: Returns detailed data using SchoolDetailSerializer.
        """
        if self.action == 'list':
            return SchoolListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SchoolInputSerializer
        return SchoolDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic during object creation (POST).
        - Saves the serializer data to create a new School instance in the database.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic during object update (PATCH).
        - Saves the serializer data to update an existing School instance in the database.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic during object deletion (DELETE).
        - Deletes the specified School instance from the database.
        """
        instance.delete()
