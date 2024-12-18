from rest_framework import serializers
from api.models import School, Spell
from django.urls import reverse


class SpellListForSchoolSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Spell
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.id]))


class SchoolDetailSerializer(serializers.ModelSerializer):
    spells = SpellListForSchoolSerializer(many=True, read_only=True)  # Related spells using `related_name="spells"`

    class Meta:
        model = School
        fields = ['id', 'index', 'name', 'spells']
