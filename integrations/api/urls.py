from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import ExtensionFormData

routers = DefaultRouter()

# routers.register(r'^form-data/', ExtensionFormData, base_name='form_data')

urlpatterns = routers.urls

urlpatterns += [
    url(r"^form-data/", ExtensionFormData.as_view()),
]
