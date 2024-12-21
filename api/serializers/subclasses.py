from rest_framework import serializers
from django.urls import reverse
from api.models import Subclass, SubclassDescription, Class


# Serializer to display a list of subclasses with basic details.
class SubclassListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Subclass
        fields = ['id', 'index', 'name', 'detail_url']  # Minimal fields for listing

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the subclass detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))


# Serializer for displaying the description of a subclass.
class SubclassDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubclassDescription
        fields = '__all__'  # Include all fields


# Serializer for creating and updating subclasses (input serializer).
class SubclassInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subclass
        fields = '__all__'  # Allow all fields for input operations


# Serializer to display detailed information about a subclass (read-only).
class SubclassDetailSerializer(serializers.ModelSerializer):
    description = SubclassDescriptionSerializer(read_only=True)
    class_info = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Subclass
        fields = '__all__'  # Include all fields with additional custom logic

    def get_detail_url(self, obj):
        """
        Returns the absolute URL for the subclass detail endpoint.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))

    def get_class_info(self, obj):
        """
        Returns information about the parent class associated with this subclass.
        Includes the class ID, name, and detail URL.
        """
        if obj.class_obj:  # Check if the subclass is linked to a parent class.
            return {
                'id': obj.class_obj.id,
                'name': obj.class_obj.name,
                'detail_url': self.context['request'].build_absolute_uri(
                    reverse('class-detail', args=[obj.class_obj.id])
                ),
            }
        return None  # Return None if no parent class is associated
