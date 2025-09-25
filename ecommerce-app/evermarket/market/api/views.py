from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from ..models import Store, Product, Review
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """All users can see all stores."""
        return Store.objects.all()

    def perform_create(self, serializer):
        """Vendor creating a store: assign the logged-in user as owner."""
        if not self.request.user.has_perm("market.add_store"):
            raise PermissionDenied(
                "You do not have permission to create stores."
            )
        serializer.save(owner=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """All users can see all products."""
        return Product.objects.all()

    def perform_create(self, serializer):
        store = serializer.validated_data["store"]
        if store.owner != self.request.user:
            raise PermissionDenied("You do not own this store.")
        if not self.request.user.has_perm("market.add_product"):
            raise PermissionDenied(
                "You do not have permission to add products."
            )
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        # Prevent vendors from posting reviews through the api
        if not self.request.user.has_perm("market.add_review"):
            raise PermissionDenied(
                "You don't have permission to post a review."
            )
        serializer.save(user=self.request.user)
