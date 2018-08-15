
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

from den.settings.base import get_env_variable


schema_view = get_swagger_view(title='Hustlers Den API')

# project level imports
from den.settings.base import ADMIN_SITE_HEADER


admin.site.site_header = ADMIN_SITE_HEADER

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^auth/login/$', obtain_jwt_token),
    # url(r'^knowledge/api/', include('knowledge.api.urls')),
    url(r'^api/knowledge/', include('knowledge.api.urls')),
    url(r'^api/integrations/', include('integrations.api.urls')),
    path(r'docs/', include_docs_urls(title='Hustlers Den API')),
    path(r'swagger-docs/', schema_view),
]


if get_env_variable('DEBUG_TOOLBAR'):
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns