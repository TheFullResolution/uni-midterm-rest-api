from api.models import School
from api.serializers.schools import SchoolListSerializer, SchoolDetailSerializer, SchoolInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class SchoolViewSet(NoPutModelViewSet):
    """
    ViewSet for managing School objects.
    - List View: Uses SchoolListSerializer.
    - Detail View: Uses SchoolDetailSerializer.
    - Create/Update: Uses SchoolInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = School.objects.all()

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the action.
        """
        if self.action == 'list':
            return SchoolListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SchoolInputSerializer
        return SchoolDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic during object creation (POST).
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic during object update (PATCH or PUT).
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic during object deletion (DELETE).
        """
        instance.delete()
