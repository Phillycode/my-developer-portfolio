from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating Note objects.

    Fields:
    - content: TextField for the note content.

    Meta class:
    - Defines the model to use (Note) and the fields to
    include in the form.

    :param forms.ModelForm: Django's ModelForm class.

    Widgets:
    - placeholder: Displays "Optional" to the user within
    the 'title' form so they know it's not required.
    """

    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Optional"}),
        }
