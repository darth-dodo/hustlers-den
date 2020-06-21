from django.conf.urls import include, url
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token

# project level imports
from den.settings.base import ADMIN_SITE_HEADER, get_env_variable

admin.site.site_header = ADMIN_SITE_HEADER
schema_view = get_schema_view(
    openapi.Info(
        title="Hustlers Den API",
        default_version="v1",
        description="API documentation for Hustlers Den",
        contact=openapi.Contact(url="https://github.com/darth-dodo/"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url("grappelli/", include("grappelli.urls")),  # grappelli URLS
    url(r"^", admin.site.urls),
    url(r"^auth/login/$", obtain_jwt_token),
    url(r"^api/knowledge/", include("knowledge.api.urls")),
    url(r"^api/integrations/", include("integrations.api.urls")),
    url(r"^api/hustlers/", include("hustlers.api.urls")),
]

# swagger urls
urlpatterns += [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger-docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

if get_env_variable("DEBUG_TOOLBAR"):
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)),] + urlpatterns
