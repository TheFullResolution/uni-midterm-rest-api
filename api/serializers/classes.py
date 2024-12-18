from rest_framework import serializers
from django.urls import reverse

from api.serializers.proficiencies import ProficiencySerializer
from api.models import Class, Subclass, SubclassDescription, SpellClass, Proficiency, ClassProficiency


class ClassSpellSerializer(serializers.ModelSerializer):
    spell_name = serializers.CharField(source="spell.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = ['id', 'spell_name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.spell.id]))


class SubclassDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubclassDescription
        fields = ['value']


class SubclassSerializer(serializers.ModelSerializer):
    description = SubclassDescriptionSerializer()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Subclass
        fields = ['id', 'index', 'name', 'subclass_flavor', 'description', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('subclass-detail', args=[obj.id]))


class ClassListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))


class ClassDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class_proficiencies = serializers.SerializerMethodField()
    spells = ClassSpellSerializer(many=True)
    subclasses = SubclassSerializer(many=True)

    class Meta:
        model = Class
        fields = ['id', 'index', 'hit_die', 'name', 'class_proficiencies', 'spells', 'subclasses', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))

    def get_class_proficiencies(self, obj):
        proficiencies = ClassProficiency.objects.filter(class_obj=obj)
        return ProficiencySerializer([p.proficiency for p in proficiencies], many=True, context=self.context).data
