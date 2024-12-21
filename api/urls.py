from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework.views import APIView
from api.views import ClassViewSet, ProficiencyViewSet, RaceViewSet, SpellViewSet, SchoolViewSet, SubclassViewSet


class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        """
        Return a custom API root view with an embedded overview and endpoint details.
        """

        class ApiRoot(APIView):
            renderer_classes = [TemplateHTMLRenderer]
            template_name = "api_root.html"

            def get(self, request, *args, **kwargs):
                # Data to pass to the template
                context = {
                    "overview": "This is a REST API built on top of a subset of D&D rules. "
                                "The subset of data was adapted from the open-source project at "
                                "<a href='https://5e-bits.github.io/docs/' target='_blank'>https://5e-bits.github.io/docs/</a>. "
                                "Their data used a NoSQL JSON structure, while this project adapts it into a relational SQL database using SQLite.",
                    "endpoints": [
                        {
                            "name": "Classes",
                            "url": request.build_absolute_uri('classes/'),
                            "methods": ["GET", "POST", "PATCH", "DELETE"],
                            "description": "Endpoints for managing character classes, e.g., Wizard, Fighter.",
                            "relations": "Each class can have subclasses and associated proficiencies.",
                        },
                        {
                            "name": "Proficiencies",
                            "url": request.build_absolute_uri('proficiencies/'),
                            "methods": ["GET", "POST", "PATCH", "DELETE"],
                            "description": "Endpoints for managing proficiencies such as skills or tools.",
                            "relations": "Linked to classes and races to define their capabilities.",
                        },
                        {
                            "name": "Races",
                            "url": request.build_absolute_uri('races/'),
                            "methods": ["GET", "POST", "PATCH", "DELETE"],
                            "description": "Endpoints for managing character races, e.g., Elf, Dwarf.",
                            "relations": "Each race can have subraces and associated proficiencies.",
                        },
                        {
                            "name": "Spells",
                            "url": request.build_absolute_uri('spells/'),
                            "methods": ["GET", "POST", "PATCH", "DELETE"],
                            "description": "Endpoints for managing spells, e.g., Fireball, Mage Hand.",
                            "relations": "Spells are linked to classes and subclasses through magic schools.",
                        },
                        {
                            "name": "Schools",
                            "url": request.build_absolute_uri('schools/'),
                            "methods": ["GET", "POST", "PATCH", "DELETE"],
                            "description": "Endpoints for managing schools of magic, e.g., Evocation, Necromancy.",
                            "relations": "Each spell belongs to a school of magic.",
                        },
                        {
                            "name": "Subclasses",
                            "url": request.build_absolute_uri('subclasses/'),
                            "methods": ["GET", "POST", "PATCH", "DELETE"],
                            "description": "Endpoints for managing subclasses, e.g., Evocation Wizard.",
                            "relations": "Subclasses are linked to a parent class and can influence available spells.",
                        },
                    ]
                }
                return Response(context)

        return ApiRoot.as_view()


# Use the custom router instead of the DefaultRouter
router = CustomRouter()

# Register the viewsets as before
router.register('classes', ClassViewSet, basename='class')
router.register('proficiencies', ProficiencyViewSet, basename='proficiency')
router.register('races', RaceViewSet, basename='race')
router.register('spells', SpellViewSet, basename='spell')
router.register('schools', SchoolViewSet, basename='school')
router.register('subclasses', SubclassViewSet, basename='subclass')

urlpatterns = router.urls
