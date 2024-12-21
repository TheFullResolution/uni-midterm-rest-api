from api.models import Class, ClassProficiency, Proficiency
from api.serializers import ClassListSerializer, ClassDetailSerializer, ClassInputSerializer
from .base_viewsets import NoPutModelViewSet


class ClassViewSet(NoPutModelViewSet):
    """
    ViewSet for handling Class data.
    - List View: Uses ClassListSerializer.
    - Detail View: Uses ClassDetailSerializer.
    - Create/Update: Uses ClassInputSerializer with support for relational links.
    - Supports POST, PATCH, and DELETE actions.
    """
    queryset = Class.objects.prefetch_related('class_proficiencies__proficiency', 'subclasses', 'spells').all()

    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the action.
        """
        if self.action == 'list':
            return ClassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClassInputSerializer
        return ClassDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Class instance, handling relational links.
        """
        proficiencies = self.request.data.get('proficiencies', [])
        class_instance = serializer.save()
        if proficiencies:
            for proficiency_id in proficiencies:
                try:
                    proficiency = Proficiency.objects.get(id=proficiency_id)
                    ClassProficiency.objects.create(class_obj=class_instance, proficiency=proficiency)
                except Proficiency.DoesNotExist:
                    # Handle gracefully or log the issue.
                    pass
        class_instance.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Class instance, handling relational links.
        """
        proficiencies = self.request.data.get('proficiencies', None)
        class_instance = serializer.save()
        if proficiencies is not None:
            # Clear existing proficiencies and add the new ones
            class_instance.class_proficiencies.all().delete()
            for proficiency_id in proficiencies:
                try:
                    proficiency = Proficiency.objects.get(id=proficiency_id)
                    ClassProficiency.objects.create(class_obj=class_instance, proficiency=proficiency)
                except Proficiency.DoesNotExist:
                    # Handle gracefully or log the issue.
                    pass
        class_instance.save()

    def perform_destroy(self, instance):
        """
        Custom logic for deleting a Class instance.
        """
        # Cascade deletion ensures related objects are deleted as necessary.
        instance.delete()
