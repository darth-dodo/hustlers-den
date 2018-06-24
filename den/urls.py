
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token

# project level imports
from den.settings.base import ADMIN_SITE_HEADER


admin.site.site_header = ADMIN_SITE_HEADER

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^auth/login/$', obtain_jwt_token),
    # url(r'^knowledge/api/', include('knowledge.api.urls')),
    url(r'^api/knowledge/', include('knowledge.api.urls')),
]
