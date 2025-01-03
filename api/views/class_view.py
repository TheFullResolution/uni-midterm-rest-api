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
    - List: Returns a summarized view of all classes.
    - Detail: Returns detailed information.
    - Create/Update: Relies on ClassInputSerializer for linking proficiencies.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Class.objects.prefetch_related(
        'class_proficiencies__proficiency',
        'subclasses',
        'spells'
    ).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ClassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClassInputSerializer
        return ClassDetailSerializer

    def perform_create(self, serializer):
        # We rely on the serializer to handle proficiencies.
        serializer.save()

    def perform_update(self, serializer):
        # Same here: the serializer handles clearing and adding proficiencies.
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
