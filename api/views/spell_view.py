from api.models import Spell
from api.serializers.spells import SpellListSerializer, SpellDetailSerializer, SpellInputSerializer
from api.views.base_viewsets import NoPutModelViewSet


class SpellViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for Spell instances.
    - List View: Uses SpellListSerializer to return basic information about spells.
    - Detail View: Uses SpellDetailSerializer to provide comprehensive details about a single spell.
    - Create/Update: Uses SpellInputSerializer to handle input for creating or updating spells.
    - Supports POST, PATCH, and DELETE actions. Excludes PUT by inheriting NoPutModelViewSet.
    """
    # QuerySet defining the data source for this ViewSet. Retrieves all Spell objects from the database.
    queryset = Spell.objects.all()

    def get_serializer_class(self):
        """
        Determines and returns the appropriate serializer class based on the action being performed.
        - 'list': Uses SpellListSerializer for summarized spell data.
        - 'create', 'update', 'partial_update': Uses SpellInputSerializer for handling input data.
        - Default: Uses SpellDetailSerializer for detailed views.
        """
        if self.action == 'list':
            return SpellListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SpellInputSerializer
        return SpellDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Spell instance.
        - Saves the serialized data to create a new Spell object in the database.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Spell instance.
        - Saves the serialized data to update an existing Spell object in the database.
        - Supports PATCH operations, as full-object replacements are excluded by design.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Spell instance.
        - Removes the specified Spell object from the database.
        """
        instance.delete()
