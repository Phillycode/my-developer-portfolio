from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, ProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet, basename="store")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls
