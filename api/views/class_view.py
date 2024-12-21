from api.models import Class, ClassProficiency, Proficiency
from api.serializers import ClassListSerializer, ClassDetailSerializer, ClassInputSerializer
from .base_viewsets import NoPutModelViewSet


class ClassViewSet(NoPutModelViewSet):
    """
    Handles CRUD operations for Class instances.
    - List: Returns a summarized view of all classes using ClassListSerializer.
    - Detail: Returns detailed information using ClassDetailSerializer.
    - Create/Update: Allows input with relational data using ClassInputSerializer.
    - Supports POST, PATCH, and DELETE actions.
    """
    # QuerySet prefetches related data to optimize database queries.
    queryset = Class.objects.prefetch_related('class_proficiencies__proficiency', 'subclasses', 'spells').all()

    def get_serializer_class(self):
        """
        Determines the serializer class based on the requested action.
        - 'list': Uses ClassListSerializer for a summarized view.
        - 'create', 'update', 'partial_update': Uses ClassInputSerializer to handle input data.
        - Default: Uses ClassDetailSerializer for detailed views.
        """
        if self.action == 'list':
            return ClassListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ClassInputSerializer
        return ClassDetailSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a Class instance.
        - Saves the instance.
        - Links proficiencies provided in the request data to the new Class instance.
        """
        proficiencies = self.request.data.get('proficiencies', [])
        class_instance = serializer.save()  # Saves the main Class instance.
        if proficiencies:
            for proficiency_id in proficiencies:
                try:
                    # Fetch the proficiency and link it to the class.
                    proficiency = Proficiency.objects.get(id=proficiency_id)
                    ClassProficiency.objects.create(class_obj=class_instance, proficiency=proficiency)
                except Proficiency.DoesNotExist:
                    # Logs or handles invalid proficiency IDs gracefully.
                    pass
        class_instance.save()

    def perform_update(self, serializer):
        """
        Custom logic for updating a Class instance.
        - Clears and reassigns relational links for proficiencies.
        """
        proficiencies = self.request.data.get('proficiencies', None)
        class_instance = serializer.save()  # Updates the main Class instance.
        if proficiencies is not None:
            # Remove existing proficiency links and add new ones.
            class_instance.class_proficiencies.all().delete()
            for proficiency_id in proficiencies:
                try:
                    # Fetch the proficiency and re-link it to the class.
                    proficiency = Proficiency.objects.get(id=proficiency_id)
                    ClassProficiency.objects.create(class_obj=class_instance, proficiency=proficiency)
                except Proficiency.DoesNotExist:
                    # Logs or handles invalid proficiency IDs gracefully.
                    pass
        class_instance.save()

    def perform_destroy(self, instance):
        """
        Handles the deletion of a Class instance.
        - Related objects are automatically deleted due to cascade settings in the models.
        """
        instance.delete()
