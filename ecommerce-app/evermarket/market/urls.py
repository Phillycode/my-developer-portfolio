from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    # Register & Login
    path("register/", views.register_user, name="register"),
    path("", views.login_user, name="login"),
    path("welcome/", views.welcome, name="welcome"),
    path("logout/", views.logout_user, name="logout"),
    # No permission view
    path("no-permission/", views.no_permission, name="no_permission"),
    # Product urls for Buyers
    path("products/", views.products_list, name="products"),
    path(
        "products/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),
    # Cart & Checkout
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    # Password reset
    path(
        "forgot_password/",
        views.forgot_password_form,
        name="forgot_password_form",
    ),
    path(
        "reset_password/",
        views.send_password_reset,
        name="password_reset_request",
    ),
    path(
        "forgot_password_sent/",
        views.forgot_password_sent,
        name="forgot_password_sent",
    ),
    path(
        "send_password_reset/",
        views.send_password_reset,
        name="send_password_reset",
    ),
    path(
        "reset_password/<str:token>/",
        views.reset_user_password,
        name="password_reset",
    ),
    # Reviews
    path("review/<int:product_id>/", views.add_review, name="add_review"),
    # Product urls for Vendors
    path("add_product/", views.add_product, name="add_product"),
    path("products/manage/", views.manage_products, name="manage_products"),
    path(
        "products/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product",
    ),
    path(
        "products/delete/<int:product_id>/",
        views.delete_product,
        name="delete_product",
    ),
    # Store urls for Vendors
    path("create-store/", views.create_store, name="create_store"),
    path("stores/", views.view_stores, name="view_stores"),
    path("stores/edit/<int:store_id>/", views.edit_store, name="edit_store"),
    path(
        "stores/delete/<int:store_id>/",
        views.delete_store,
        name="delete_store",
    ),
]
