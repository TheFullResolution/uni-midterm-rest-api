from rest_framework import serializers
from django.urls import reverse
from api.models import Proficiency, ProficiencyClass, ProficiencyRace


class ProficiencySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        fields = '__all__'
        depth = 2

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


class ProficiencyClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="class_obj.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = ProficiencyClass
        fields = ['class_name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')  # Get the request context
        return request.build_absolute_uri(reverse('class-detail', args=[obj.class_obj.id]))


# Serializer for related Race and Subrace (used in ProficiencyDetailSerializer)
class ProficiencyRaceSerializer(serializers.ModelSerializer):
    race_name = serializers.CharField(source="race.name", read_only=True)
    subrace_name = serializers.CharField(source="subrace.name", read_only=True)

    class Meta:
        model = ProficiencyRace
        fields = ['race_name', 'subrace_name']


# Minimal Proficiency List Serializer
class ProficiencyListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Proficiency
        fields = ['id', 'name', 'type', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.id]))


# Detailed Proficiency Serializer
class ProficiencyDetailSerializer(serializers.ModelSerializer):
    proficiency_classes = ProficiencyClassSerializer(many=True)
    races_and_subraces = ProficiencyRaceSerializer(many=True)

    class Meta:
        model = Proficiency
        fields = ['id', 'index', 'name', 'type', 'proficiency_classes', 'races_and_subraces']
