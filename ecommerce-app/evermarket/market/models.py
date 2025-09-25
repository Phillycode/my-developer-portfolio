from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Store(models.Model):
    """This model represents a store that can be created by a vendor"""

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stores"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional logo
    logo = models.ImageField(upload_to="store_logo/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"


class Product(models.Model):
    """Products sold by stores and added by vendors.
    Currently using an optional image attribute."""

    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional image
    image = models.ImageField(
        upload_to="product_images/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} ({self.store.name})"


class Review(models.Model):
    """Reviews are associated with a product that can be written by any
    user, but will count as unverified unless the user has
    purchased the item. Then it will count as a verified review."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)  # False by default
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class CartItem(models.Model):
    """This model represents a product that has been added to the cart
    of a buyer and has the quantity field."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} "
            f" for {self.user.username}"
        )


class Order(models.Model):
    """Order model for purposes of keeping an order history.
    Currently the main purpose is for verifying reviews."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)


class ResetToken(models.Model):
    """Reset Token model used in forgot_password flow"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
