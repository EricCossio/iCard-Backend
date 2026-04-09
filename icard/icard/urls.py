"""
URL configuration for icard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.api.router import router_user
from itinerario.api.router import router as router_itinerario

from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenRefreshView  # ← 

schema_view = get_schema_view(
   openapi.Info(
      title="iCard - api Doc",
      default_version='v1',
      description="Documentacion de la api de iCard",
      terms_of_service="https://www.tincode.es/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_user.urls)),
    path('api/', include(router_itinerario.urls)),
    path('api/', include('users.api.router')),      # auth/login, auth/register, auth/me
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ← agregar
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]