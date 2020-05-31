from rest_framework.routers import DefaultRouter

from hustlers.api.views import HustlerViewSet

router = DefaultRouter()

router.register(r"^hustler", HustlerViewSet)

urlpatterns = router.urls
