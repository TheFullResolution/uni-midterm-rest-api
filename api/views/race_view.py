from api.models import Race
from api.serializers import RaceListSerializer, RaceDetailSerializer, RaceInputSerializer
from .base_viewsets import NoPutModelViewSet


class RaceViewSet(NoPutModelViewSet):
    """
    ViewSet for managing Race objects.
    - List View: Uses RaceListSerializer.
    - Detail View: Uses RaceDetailSerializer.
    - Create/Update: Uses RaceInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Race.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RaceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RaceInputSerializer
        return RaceDetailSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
