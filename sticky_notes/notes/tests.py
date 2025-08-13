from django.test import TestCase
from django.urls import reverse
from .models import Note


# Tests here
class NoteModelTest(TestCase):
    """This test class tests whether our Note model functions as
    intended and also tests 'create' and 'delete' functionality for
    our sticky notes."""

    def setUp(self):
        # Create a Note object for initial "create" testing
        Note.objects.create(
            title="Test Sticky 1", content="This is a test sticky."
        )
        # Create a Note object without a title
        Note.objects.create(content="This is a test sticky 2.")

    def test_note_has_title(self):
        # Test that a Note object has the expected title
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, "Test Sticky 1")

    def test_note_has_content(self):
        # Test that a Note object has the expected content
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, "This is a test sticky.")

    def test_note_has_no_title(self):
        # Test that a Note object has no title after being
        # successfully added to database.
        note = Note.objects.get(id=2)
        self.assertIsNone(note.title)

    def test_note_without_title_has_content(self):
        # Test that a Note object has content
        # despite having no title.
        note = Note.objects.get(id=2)
        self.assertEqual(note.content, "This is a test sticky 2.")

    def test_note_deletion(self):
        note = Note.objects.get(id=2)
        note.delete()
        # Test that the note is gone from database
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=2)


class NoteViewTest(TestCase):
    """This test class tests whether our views are working
    correctly and is responsible for testing our 'read' and
    'update' use cases."""

    def setUp(self):
        # Create an instance variable (self.note) to hold our
        # note object for reuse in multiple tests.
        self.note = Note.objects.create(
            title="Test Sticky", content="This is a test sticky."
        )

    def test_note_list_view(self):
        # Test the note_list view
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Sticky")

    def test_note_detail_view(self):
        # Test the note_detail view
        response = self.client.get(reverse("note_detail", args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Sticky")
        self.assertContains(response, "This is a test sticky.")

    def test_note_update_view(self):
        # Test updating a note
        update_url = reverse("note_update", args=[self.note.pk])
        response = self.client.post(
            update_url,
            {"title": "Updated Sticky", "content": "Updated content."},
        )

        # Check if view redirects to note_list
        self.assertRedirects(response, reverse("note_list"))

        # Refresh from database and check updated values
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Sticky")
        self.assertEqual(self.note.content, "Updated content.")
