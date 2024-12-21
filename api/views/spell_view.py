from api.models import Spell
from api.serializers.spells import SpellListSerializer, SpellDetailSerializer, SpellInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class SpellViewSet(NoPutModelViewSet):
    """
    ViewSet for managing Spell objects.
    - List View: Uses SpellListSerializer.
    - Detail View: Uses SpellDetailSerializer.
    - Create/Update: Uses SpellInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Spell.objects.all()

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the action.
        """
        if self.action == 'list':
            return SpellListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SpellInputSerializer
        return SpellDetailSerializer

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
