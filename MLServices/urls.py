"""
URL configuration for MLServices project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from app_credito_banco.View import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API para predicción de crédito en una institución financiera",
      default_version='v1',
      description="Es el API para predicción de crédito en una institución financiera",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="remigiohurtado@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('appmarketing/', include('app_marketing_banco.urls')),
    path('nuevasolicitud/', views.Clasificacion.determinarAprobacion, name='nuevasolicitud'),
    # re_path(r'^nuevasolicitud/$',views.Clasificacion.determinarAprobacion),
    re_path(r'^predecir/',views.Clasificacion.predecir),
    re_path(r'^predecirIOJson/',views.Clasificacion.predecirIOJson),
]