from rest_framework.routers import DefaultRouter

from knowledge.api.views import CategoryViewSet, ExpertiseLevelViewSet, MediaTypeViewSet, KnowledgeStoreViewSet

router = DefaultRouter()

router.register(r'^category', CategoryViewSet)
router.register(r'^media-type', MediaTypeViewSet)
router.register(r'^expertise-level', ExpertiseLevelViewSet)
router.register(r'^knowledge-store', KnowledgeStoreViewSet)

urlpatterns = router.urls
