import secrets
from datetime import timedelta
from django.utils import timezone
from hashlib import sha1
from .models import ResetToken
from django.contrib.auth.models import Group, Permission


# Generate encrypted token for password reset
def generate_reset_url(user):
    """This function is responsible for creating a unique token
    object when a user requests a password reset.
    - The token is stored as 'hashed' in our database.
    - The unhashed token is sent in the email."""

    domain = "http://127.0.0.1:8000"
    app_name = ""
    reset_url = f"{domain}{app_name}/reset_password/"
    token = str(secrets.token_urlsafe(16))
    # Create expiry date/time using a timezone-aware value
    expiry_date = timezone.now() + timedelta(minutes=5)
    ResetToken.objects.create(
        user=user,
        token=sha1(token.encode()).hexdigest(),
        expiry_date=expiry_date,
    )
    reset_url += f"{token}/"
    return reset_url


# Create groups (Vendors, Buyers) and add permissions
def setup_group_permissions(sender, **kwargs):
    roles_permissions = {
        "Vendors": [
            "add_product",
            "change_product",
            "view_product",
            "delete_product",
            "add_store",
            "view_store",
            "change_store",
            "delete_store",
        ],
        "Buyers": [
            "view_product",
            "view_cartitem",
            "add_cartitem",
            "change_cartitem",
            "delete_cartitem",
            "view_review",
            "add_review",
        ],
    }

    for role, perm_codenames in roles_permissions.items():
        group, _ = Group.objects.get_or_create(name=role)
        perms = Permission.objects.filter(
            content_type__app_label="market",
            codename__in=perm_codenames,
        )
        # Adds missing permissions only
        group.permissions.add(*perms)
    print("Group permissions have been set.")
