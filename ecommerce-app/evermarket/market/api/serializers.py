from rest_framework import serializers
from ..models import Store, Product, Review


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)  # Shows username
    products = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )  # List product IDs

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "owner",
            "description",
            "created_at",
            "products",
        ]


class ProductSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "store",
            "description",
            "price",
            "stock",
            "created_at",
            "image",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows username
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "rating",
            "comment",
            "verified",
            "created_at",
        ]
