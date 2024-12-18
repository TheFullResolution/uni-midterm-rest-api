from rest_framework import serializers
from django.urls import reverse
from api.models import Race, Subrace, RaceStartingProficiency


class RaceListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields = ['id', 'index', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))


class SubraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrace
        fields = ['id', 'index', 'name', 'desc']


class RaceStartingProficiencySerializer(serializers.ModelSerializer):
    proficiency_name = serializers.CharField(source="proficiency.name", read_only=True)
    proficiency_url = serializers.SerializerMethodField()

    class Meta:
        model = RaceStartingProficiency
        fields = ['proficiency_name', 'proficiency_url']

    def get_proficiency_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.proficiency.id]))


class RaceDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    subraces = SubraceSerializer(many=True)
    starting_proficiencies = RaceStartingProficiencySerializer(many=True)

    class Meta:
        model = Race
        fields = [
            'id',
            'index',
            'name',
            'age',
            'alignment',
            'language_desc',
            'size',
            'size_description',
            'speed',
            'subraces',
            'starting_proficiencies',
            'detail_url',
        ]

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('race-detail', args=[obj.id]))
