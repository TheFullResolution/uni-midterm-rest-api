from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .api import ClassViewSet, ProficiencyViewSet, RaceViewSet, SpellViewSet, SchoolViewSet

router = DefaultRouter()
router.register('classes', ClassViewSet, basename='class')
router.register('proficiencies', ProficiencyViewSet, basename='proficiency')
router.register('races', RaceViewSet, basename='race')
router.register('spells', SpellViewSet, basename='spell')
router.register('schools', SchoolViewSet, basename='school')

urlpatterns = [
    # Redirect root URL to the API page
    path('', RedirectView.as_view(url='/api/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),

]
