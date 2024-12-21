from api.models import Subclass
from api.serializers.subclasses import SubclassListSerializer, SubclassDetailSerializer, SubclassInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class SubclassViewSet(NoPutModelViewSet):
    """
    ViewSet for managing Subclass objects.
    - List View: Uses SubclassListSerializer.
    - Detail View: Uses SubclassDetailSerializer.
    - Create/Update: Uses SubclassInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Subclass.objects.all()

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the action.
        """
        if self.action == 'list':
            return SubclassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubclassInputSerializer
        return SubclassDetailSerializer

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
