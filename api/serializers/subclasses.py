from rest_framework import serializers
from django.urls import reverse

from api.models import Subclass, SubclassDescription, Class


# Serializer to display a list of subclasses with basic details.
class SubclassListSerializer(serializers.ModelSerializer):
    # Provides the detail URL for each subclass.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Subclass
        # Specifies the fields to include in the serialized output.
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the subclass detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))


# Serializer for displaying the description of a subclass.
class SubclassDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubclassDescription
        # Specifies the field to include in the serialized output.
        fields = ['value']  # Contains the textual description of the subclass.


# Serializer to display detailed information about a subclass.
class SubclassDetailSerializer(serializers.ModelSerializer):
    # Serializes the description of the subclass.
    description = SubclassDescriptionSerializer()
    # Provides information about the parent class linked to this subclass.
    class_info = serializers.SerializerMethodField()
    # Provides the detail URL for the subclass.
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Subclass
        # Specifies the fields to include in the serialized output.
        fields = [
            'id',  # Unique identifier of the subclass.
            'index',  # Index field for external referencing.
            'name',  # Name of the subclass.
            'subclass_flavor',  # Flavor or theme of the subclass, e.g., "Evocation".
            'description',  # Detailed description of the subclass.
            'class_info',  # Information about the associated parent class.
            'detail_url',  # Detail URL for the subclass.
        ]

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the subclass detail endpoint.
        The URL is dynamically built using the current request context.
        """
        request = self.context.get('request')  # Access the current request context.
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))

    def get_class_info(self, obj):
        """
        Returns information about the parent class associated with this subclass.
        Includes the class ID, name, and detail URL.
        """
        if obj.class_obj:  # Check if the subclass is linked to a parent class.
            return {
                'id': obj.class_obj.id,  # Unique identifier of the class.
                'name': obj.class_obj.name,  # Name of the class.
                'detail_url': self.context['request'].build_absolute_uri(
                    reverse('class-detail', args=[obj.class_obj.id])  # Build the detail URL for the class.
                ),
            }
        return None  # Return None if no parent class is associated.
