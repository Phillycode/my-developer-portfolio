from django.db import models


# Create your models here.
class Note(models.Model):
    """Model representing a sticky note posted in the app. I'm going
    with a simple text/content-only sticky note to work as easy
    and simple reminders.

    Fields:
    - title: Title is optional and max 100 characters
    - content: TextField for the post content.
    - created_at: DateTimeField set to the current date and time
    when the post is created.
    """

    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Return the primary key assigned to the note by Django.
    def __str__(self):
        # Check if title is assigned
        if self.title:
            return self.title
        # Else, return primary key assigned by Django
        else:
            return f"Sticky Note {self.id}"
