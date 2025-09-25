from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils import timezone
from .utils import generate_reset_url
from .models import Product, CartItem, ResetToken, Order, Store
from .emails import EmailBuilder
from .forms import RegisterForm, ReviewForm, StoreForm, ProductForm
from django.contrib import messages
from decimal import Decimal
from hashlib import sha1
from .functions.twitter import Tweet


# Register new user
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Assign selected group
            role = form.cleaned_data.get("role")
            if role:
                group = Group.objects.get(name=role)
                user.groups.add(group)

            login(request, user)
            return redirect("market:welcome")
    else:
        form = RegisterForm()
    return render(request, "market/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Use Django's login function
            login(request, user)
            return redirect("market:welcome")
    else:
        form = AuthenticationForm()
    return render(request, "market/login.html", {"form": form})


@login_required
def logout_user(request):
    # Use Django's logout function
    logout(request)
    return redirect("market:login")


def welcome(request):
    if request.user.is_authenticated:
        user_groups = request.user.groups.values_list("name", flat=True)
        return render(
            request, "market/welcome.html", {"user_groups": user_groups}
        )
    else:
        return redirect("market:login")


# Forgot pw flow 1
def forgot_password_form(request):
    return render(request, "market/forgot_password_form.html")


# Forgot pw flow 2
def send_password_reset(request):
    user_email = request.POST.get("email")

    try:
        user = User.objects.get(email=user_email)
        reset_url = generate_reset_url(user)
        reset_email = EmailBuilder.build_pw_reset_email(user, reset_url)
        reset_email.send()
    except User.DoesNotExist:
        # Do nothing if email isn't found (security best practice)
        pass

    # Always redirect to "email sent" confirmation
    return redirect("market:forgot_password_sent")


# Forgot pw flow 3
def forgot_password_sent(request):
    return render(request, "market/forgot_password_sent.html")


# Forgot pw flow 4
# When user clicks password reset link
def reset_user_password(request, token):
    """
    Handles password reset:
    - Verifies the token
    - Lets the user submit a new password
    """
    token_hashed = sha1(token.encode()).hexdigest()

    try:
        reset_token = ResetToken.objects.get(token=token_hashed, used=False)
    except ResetToken.DoesNotExist:
        return HttpResponse("Invalid or expired token", status=400)

    # Check for token expiry
    if reset_token.expiry_date < timezone.now():
        return HttpResponse("Token has expired", status=400)

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not new_password or new_password != confirm_password:
            return HttpResponse("Passwords do not match", status=400)

        # Update the user's password
        reset_token.user.password = make_password(new_password)
        reset_token.user.save()

        # Mark token as used
        reset_token.used = True
        reset_token.save()

        return render(request, "market/password_reset_success.html")

    # GET request to show form
    return render(request, "market/reset_password_form.html", {"token": token})


# Products list - Keeping it public for now
def products_list(request):
    products = Product.objects.all()
    return render(request, "market/products.html", {"products": products})


# Product detail - Public
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()

    return render(
        request,
        "market/product_detail.html",
        {"product": product, "reviews": reviews},
    )


@login_required
# View to show that the user doesn't have permission for the page.
def no_permission(request):
    return render(request, "market/no_permission.html")


@login_required
def add_to_cart(request, product_id):
    # Check permission
    if not request.user.has_perm("market.add_cartitem"):
        return redirect("market:no_permission")
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})

    # Get quantity from form (default = 1 if missing/invalid)
    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    # If product already in cart, increase quantity
    if str(product.id) in cart:
        cart[str(product.id)]["quantity"] += quantity
    else:
        cart[str(product.id)] = {
            "name": product.name,
            "price": str(product.price),  # Str for JSON serialization
            "quantity": quantity,
        }

    request.session["cart"] = cart
    return redirect("market:view_cart")


@login_required
# Display all cart items for the logged-in user
def view_cart(request):
    if not request.user.has_perm("market.view_cartitem"):
        return redirect("market:no_permission")
    cart = request.session.get("cart", {})
    for item in cart.values():
        item["subtotal"] = Decimal(item["price"]) * item["quantity"]

    total = sum(item["subtotal"] for item in cart.values())
    return render(request, "market/cart.html", {"cart": cart, "total": total})


# Remove a cart item
@login_required
def remove_from_cart(request, item_id):
    if not request.user.has_perm("market.delete_cartitem"):
        return redirect("market:no_permission")
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
    return redirect("market:view_cart")


@login_required
# Ensure atomicity (no partial stock updates)
@transaction.atomic
def checkout(request):
    if not request.user.has_perm("market.add_cartitem"):
        return redirect("market:no_permission")

    cart = request.session.get("cart", {})

    # Check if cart is empty
    if not cart:
        return HttpResponse("Your cart is empty.", status=400)

    # Check stock availability
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        if item["quantity"] > product.stock:
            return HttpResponse(
                f"Not enough stock for {product.name}. "
                f"Available: {product.stock}, Requested: {item['quantity']}",
                status=400,
            )

    # Subtract from stock and create Order objects
    # to remember purchase history of user.
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        product.stock -= item["quantity"]
        product.save()

        # Create Order object
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=item["quantity"],
        )

    # Send invoice
    email = EmailBuilder.build_invoice_email(request.user, cart)
    email.send()

    # Clear session cart
    request.session["cart"] = {}

    # Redirect to success page
    return redirect("market:checkout_success")


@login_required
def checkout_success(request):
    return render(request, "market/checkout_success.html")


@login_required
def add_review(request, product_id):
    if not request.user.has_perm("market.add_review"):
        return redirect("market:no_permission")
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            # Check if user purchased this product via bool value
            review.verified = Order.objects.filter(
                user=request.user, product=product
            ).exists()
            review.save()
            return redirect("market:product_detail", product_id=product.id)
    else:
        form = ReviewForm()
    return render(
        request, "market/add_review.html", {"form": form, "product": product}
    )


@login_required
def create_store(request):
    if not request.user.has_perm("market.add_store"):
        return redirect("market:no_permission")
    if request.method == "POST":
        # Use request.FILES to handle logo upload
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            # Tweet about new store
            tweet_store(store)
            return redirect("market:view_stores")
    else:
        form = StoreForm()
    return render(request, "market/create_store.html", {"form": form})


@login_required
def view_stores(request):
    stores = Store.objects.filter(owner=request.user)
    return render(request, "market/view_stores.html", {"stores": stores})


@login_required
def edit_store(request, store_id):
    if not request.user.has_perm("market.change_store"):
        return redirect("market:no_permission")
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == "POST":
        # Use request.FILES to handle logo upload
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return redirect("market:view_stores")
    else:
        form = StoreForm(instance=store)
    return render(
        request, "market/edit_store.html", {"form": form, "store": store}
    )


@login_required
def delete_store(request, store_id):
    if not request.user.has_perm("market.delete_store"):
        return redirect("market:no_permission")
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == "POST":
        store.delete()
        messages.success(request, "Store deleted successfully.")
        return redirect("market:view_stores")
    return render(request, "market/delete_store.html", {"store": store})


@login_required
def add_product(request):
    if not request.user.has_perm("market.add_product"):
        return redirect("market:no_permission")
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Ensure vendor owns the store
            if product.store.owner == request.user:
                product.save()
                # Tweet about new product
                tweet_product(product)
                # Redirect after success
                return redirect("market:manage_products")
            else:
                form.add_error(
                    "store", "You can only add products to your own stores."
                )
    else:
        form = ProductForm()

        # Restrict store choices to the vendor's stores
        form.fields["store"].queryset = Store.objects.filter(
            owner=request.user
        )

    return render(request, "market/add_product.html", {"form": form})


@login_required
def manage_products(request):
    if not request.user.has_perm("market.change_product"):
        return redirect("market:no_permission")
    # Get the logged in vendor's products
    stores = Store.objects.filter(owner=request.user)
    products = Product.objects.filter(store__in=stores)

    if request.method == "POST":
        product_id = request.POST.get("delete_product_id")
        if product_id:
            product = get_object_or_404(
                Product, id=product_id, store__in=stores
            )
            product.delete()
            return redirect("market:manage_products")

    return render(
        request, "market/manage_products.html", {"products": products}
    )


@login_required
def edit_product(request, product_id):
    if not request.user.has_perm("market.change_product"):
        return redirect("market:no_permission")
    product = get_object_or_404(
        Product, id=product_id, store__owner=request.user
    )

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("market:manage_products")
    else:
        form = ProductForm(instance=product)

    return render(
        request, "market/edit_product.html", {"form": form, "product": product}
    )


@login_required
def delete_product(request, product_id):
    if not request.user.has_perm("market.delete_product"):
        return redirect("market:no_permission")
    product = get_object_or_404(Product, id=product_id)

    # Check if logged in user owns the store
    if request.user == product.store.owner:
        if request.method == "POST":
            product.delete()
            return redirect("market:manage_products")
    else:
        # Redirect if not store owner
        return redirect("market:manage_products")

    # Redirect to products after deletion
    return redirect("market:manage_products")


# Tweet when a new store gets added
def tweet_store(store):
    text = (
        f"New Store Added!\n\nName: {store.name}\nDescription: "
        f"{store.description or ''}"  # Blank description if none
    )

    media_id = None
    if store.logo:  # If optional image was added
        media_id = Tweet().upload_media(store.logo.path)

    Tweet().make_tweet(text, media_id)


# Tweet when a new product gets added to a store
def tweet_product(product):
    text = (
        f"New Product from {product.store.name}!\n\n"
        f"Name: {product.name}\nDescription: "
        f"{product.description or ''}"  # Blank description if none
    )

    media_id = None
    if product.image:  # If optional image was added
        media_id = Tweet().upload_media(product.image.path)

    Tweet().make_tweet(text, media_id)
