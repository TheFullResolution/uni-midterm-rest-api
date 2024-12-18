from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root URL to the API page
    path('', RedirectView.as_view(url='/api/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include API routes
]
