from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Review, Store, Product


class RegisterForm(UserCreationForm):
    """
    User Registration form

    - Inherits from Django's UserCreationForm
    - User can choose between buyer/vendor via RadioSelect widget
    """

    email = forms.EmailField(
        required=True, help_text="Required. Enter a valid email address."
    )

    ROLE_CHOICES = [
        ("Buyers", "Buyer"),
        ("Vendors", "Vendor"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Register as",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already associated with an account."
            )
        return email


class LoginForm(AuthenticationForm):
    """
    Form for user login.

    Inherits from Django's AuthenticationForm.
    Allows customization of widgets and labels.
    """

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        label="Password",
    )


class ReviewForm(forms.ModelForm):
    """
    Review Form for Buyers to leave reviews
    - Provides fields for rating and comment
    """

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        labels = {
            "rating": "Rating (1-5)",
            "comment": "Your Review",
        }


class StoreForm(forms.ModelForm):
    """
    Form for adding a new Store as a Vendor
    - Provides name and description fields
    """

    class Meta:
        model = Store
        fields = ["name", "description", "logo"]


class ProductForm(forms.ModelForm):
    """
    Form for adding products as a Vendor
    Provides fields for:
    - name
    - description
    - price
    - stock
    - image (optional)
    - store
    """

    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "image", "store"]
