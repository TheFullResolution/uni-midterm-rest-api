from django.urls import reverse
from rest_framework import serializers
from api.models import Class, ClassProficiency, Proficiency, SpellClass


class ClassSpellSerializer(serializers.ModelSerializer):
    spell_name = serializers.CharField(source="spell.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = SpellClass
        fields = ['id', 'spell_name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('spell-detail', args=[obj.spell.id]))


class ClassProficiencySerializer(serializers.ModelSerializer):
    proficiency_name = serializers.CharField(source="proficiency.name", read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = ClassProficiency
        fields = ['id', 'proficiency_name', 'detail_url']

    def get_detail_url(self, obj):
        """
        Returns the URL for the related Proficiency detail view.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('proficiency-detail', args=[obj.proficiency.id]))


class ClassListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))


class ClassInputSerializer(serializers.ModelSerializer):
    proficiencies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Proficiency.objects.all(),
        required=False,
    )

    class Meta:
        model = Class
        fields = ['id', 'index', 'hit_die', 'name', 'proficiencies']

    def create(self, validated_data):
        proficiencies = validated_data.pop('proficiencies', [])
        class_instance = Class.objects.create(**validated_data)
        for proficiency in proficiencies:
            ClassProficiency.objects.create(class_obj=class_instance, proficiency=proficiency)
        return class_instance

    def update(self, instance, validated_data):
        proficiencies = validated_data.pop('proficiencies', None)
        if proficiencies is not None:
            instance.class_proficiencies.all().delete()
            for proficiency in proficiencies:
                ClassProficiency.objects.create(class_obj=instance, proficiency=proficiency)
        return super().update(instance, validated_data)


class ClassDetailSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class_proficiencies = ClassProficiencySerializer(many=True, read_only=True)
    subclasses = serializers.SerializerMethodField()
    spells = ClassSpellSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'index', 'hit_die', 'name', 'detail_url', 'class_proficiencies', 'subclasses', 'spells']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('class-detail', args=[obj.id]))

    def get_subclasses(self, obj):
        """
        Returns a simplified representation of subclasses:
        URL, ID, and name.
        """
        request = self.context.get('request')
        return [
            {
                "url": request.build_absolute_uri(reverse('subclass-detail', args=[subclass.id])),
                "id": subclass.id,
                "name": subclass.name,
            }
            for subclass in obj.subclasses.all()
        ]
