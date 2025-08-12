"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from empresas.tenant_info import EmpresaInfoView
from empresas.views import EmpresaViewSet

# Importamos los ViewSets de nuestras apps
from envios.views import EnvioViewSet, HistorialEstadoViewSet
from envios.views_public import rastrear_por_guia_publico, rastrear_por_nombre_publico

# Importar health check
from health_check import health_check
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usuarios.views import UsuarioViewSet

# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Paquetería Cuba API",
        default_version="v1",
        description="API para el sistema de gestión de paquetería",
        terms_of_service="https://www.packfy.com/terms/",
        contact=openapi.Contact(email="contact@packfy.com"),
        license=openapi.License(name="Paquetería Cuba License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configurar el router de DRF
router = routers.DefaultRouter()
# Registramos los viewsets
router.register(r"envios", EnvioViewSet)
router.register(r"historial-estados", HistorialEstadoViewSet)
router.register(r"usuarios", UsuarioViewSet)
router.register(r"empresas", EmpresaViewSet)

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="/api/swagger/", permanent=False),
        name="index",
    ),
    path("admin/", admin.site.urls),
    # API endpoints
    path("api/", include(router.urls)),
    path(
        "api/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Health check endpoint
    path("api/health/", health_check, name="health_check"),
    # Endpoint para información del sistema
    path("api/sistema-info/", EmpresaInfoView.as_view(), name="sistema_info"),
    # Endpoints públicos de rastreo
    path(
        "api/public/rastrear-nombre/",
        rastrear_por_nombre_publico,
        name="rastrear_nombre_publico",
    ),
    path(
        "api/public/rastrear-guia/",
        rastrear_por_guia_publico,
        name="rastrear_guia_publico",
    ),
    # Swagger UI
    path(
        "api/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

# Configuración para servir archivos estáticos y media en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
