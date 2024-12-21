from rest_framework.routers import DefaultRouter
from api.views import (
    ClassViewSet,
    ProficiencyViewSet,
    RaceViewSet,
    SpellViewSet,
    SchoolViewSet,
    SubclassViewSet,
)

# Initialize the router for automatic URL routing of ViewSets.
router = DefaultRouter()

# Register the ClassViewSet for handling class-related endpoints.
# The basename 'class' will be used to create URL patterns like /api/classes/.
router.register('classes', ClassViewSet, basename='class')

# Register the ProficiencyViewSet for handling proficiency-related endpoints.
# The basename 'proficiency' will generate URLs like /api/proficiencies/.
router.register('proficiencies', ProficiencyViewSet, basename='proficiency')

# Register the RaceViewSet for handling race-related endpoints.
# The basename 'race' will generate URLs like /api/races/.
router.register('races', RaceViewSet, basename='race')

# Register the SpellViewSet for handling spell-related endpoints.
# The basename 'spell' will generate URLs like /api/spells/.
router.register('spells', SpellViewSet, basename='spell')

# Register the SchoolViewSet for handling school-related endpoints.
# The basename 'school' will generate URLs like /api/schools/.
router.register('schools', SchoolViewSet, basename='school')

# Register the SubclassViewSet for handling subclass-related endpoints.
# The basename 'subclass' will generate URLs like /api/subclasses/.
router.register('subclasses', SubclassViewSet, basename='subclass')

# Assign the router-generated URLs to the urlpatterns variable.
# This includes all the registered ViewSets' URL patterns.
urlpatterns = router.urls
