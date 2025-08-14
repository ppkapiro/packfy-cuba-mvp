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
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from usuarios.auth_views import (
    SecureTokenObtainPairView,
    SecureTokenRefreshView,
    change_password,
    secure_logout,
    user_profile,
)
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
    # 🔒 API de Autenticación Segura
    path(
        "api/auth/login/",
        SecureTokenObtainPairView.as_view(),
        name="secure_login",
    ),
    path(
        "api/auth/refresh/",
        SecureTokenRefreshView.as_view(),
        name="secure_refresh",
    ),
    path("api/auth/logout/", secure_logout, name="secure_logout"),
    path("api/auth/profile/", user_profile, name="user_profile"),
    path("api/auth/change-password/", change_password, name="change_password"),
    # 🚀 API endpoints principales
    path("api/", include(router.urls)),
    # 🤖 API de Inteligencia Artificial - Temporalmente deshabilitado
    # path("api/ai/", include("envios.ai_urls")),
    # 📊 Endpoint para información del sistema
    path("api/sistema-info/", EmpresaInfoView.as_view(), name="sistema_info"),
    # 📚 Swagger UI
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
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
