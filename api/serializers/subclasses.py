from rest_framework import serializers
from django.urls import reverse
from api.models import Subclass, SubclassDescription, Class


# Serializer for listing subclasses with basic information.
class SubclassListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()  # Adds a field for the detail URL of each subclass.

    class Meta:
        model = Subclass
        fields = ['id', 'index', 'name', 'detail_url']  # Exposes minimal fields for listing purposes.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the subclass detail endpoint.
        This ensures dynamic linking to detailed views of subclasses.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))


# Serializer for displaying the description associated with a subclass.
class SubclassDescriptionSerializer(serializers.ModelSerializer):
    """
    Handles the serialization of SubclassDescription objects.
    Used to represent textual descriptions of subclasses in detail views.
    """

    class Meta:
        model = SubclassDescription
        fields = '__all__'  # Includes all fields of the SubclassDescription model.


# Serializer for creating and updating subclasses (input serializer).
class SubclassInputSerializer(serializers.ModelSerializer):
    """
    Handles the serialization and validation of input data for creating or updating subclasses.
    """

    class Meta:
        model = Subclass
        fields = '__all__'  # Allows full customization of Subclass instances during input operations.


# Serializer for displaying detailed information about a subclass.
class SubclassDetailSerializer(serializers.ModelSerializer):
    description = SubclassDescriptionSerializer(read_only=True)  # Nested serializer for subclass descriptions.
    class_info = serializers.SerializerMethodField()  # Custom field for parent class information.
    detail_url = serializers.SerializerMethodField()  # Adds a field for the subclass detail URL.

    class Meta:
        model = Subclass
        fields = '__all__'  # Exposes all fields, including nested relationships and custom fields.

    def get_detail_url(self, obj):
        """
        Constructs and returns the absolute URL for the subclass detail endpoint.
        This provides dynamic linking to detailed views of subclasses.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))

    def get_class_info(self, obj):
        """
        Retrieves information about the parent class associated with this subclass.
        Includes:
        - Class ID
        - Class Name
        - Class Detail URL

        Returns None if no parent class is linked.
        """
        if obj.class_obj:  # Check if the subclass is linked to a parent class.
            return {
                'id': obj.class_obj.id,
                'name': obj.class_obj.name,
                'detail_url': self.context['request'].build_absolute_uri(
                    reverse('class-detail', args=[obj.class_obj.id])
                ),
            }
        return None  # Return None if no parent class is associated.
