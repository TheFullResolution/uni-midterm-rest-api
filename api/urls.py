from rest_framework.routers import DefaultRouter
from api.views import (
    ClassViewSet,
    ProficiencyViewSet,
    RaceViewSet,
    SpellViewSet,
    SchoolViewSet,
    SubclassViewSet,
)

router = DefaultRouter()
router.register('classes', ClassViewSet, basename='class')
router.register('proficiencies', ProficiencyViewSet, basename='proficiency')
router.register('races', RaceViewSet, basename='race')
router.register('spells', SpellViewSet, basename='spell')
router.register('schools', SchoolViewSet, basename='school')
router.register('subclasses', SubclassViewSet, basename='subclass')

urlpatterns = router.urls
