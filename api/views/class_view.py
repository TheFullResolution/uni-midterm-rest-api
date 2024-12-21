from api.models import Class
from api.serializers import ClassListSerializer, ClassDetailSerializer, ClassInputSerializer
from .base_viewsets import NoPutModelViewSet


class ClassViewSet(NoPutModelViewSet):
    """
    ViewSet for handling Class data.
    - List View: Uses ClassListSerializer.
    - Detail View: Uses ClassDetailSerializer.
    - Create/Update: Uses ClassInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Class.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ClassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClassInputSerializer
        return ClassDetailSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
