import shutil
import tempfile
from decimal import Decimal
from io import BytesIO

from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.clients.models import Client
from apps.media_assets.models import PhotoClassification
from apps.media_assets.services import create_project_photo, replace_project_photo
from apps.projects.models import Project


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProjectPhotoServiceTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="serviceuser",
            email="serviceuser@example.com",
            password="StrongPass123!",
        )

        cls.customer = Client.objects.create(
            legal_name="Service Client",
            commercial_name="Service Client",
            client_type="company",
            status="active",
            email="service-client@example.com",
            phone="0888888888",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.customer,
            opportunity=None,
            responsible=cls.user,
            name="Service Project",
            description="Testing media services",
            location="Guayaquil",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

    def _make_image(self, name="service-photo.jpg", color="green"):
        buffer = BytesIO()
        image = Image.new("RGB", (240, 240), color=color)
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")

    def test_create_project_photo_populates_metadata(self):
        photo = create_project_photo(
            project=self.project,
            image=self._make_image(),
            classification=PhotoClassification.IN_PROGRESS,
            actor=self.user,
            title="Progress evidence",
            description="Installed structure",
        )

        self.assertEqual(photo.project, self.project)
        self.assertEqual(photo.classification, PhotoClassification.IN_PROGRESS)
        self.assertEqual(photo.original_filename, "service-photo.jpg")
        self.assertEqual(photo.mime_type, "image/jpeg")
        self.assertGreater(photo.file_size, 0)
        self.assertEqual(photo.created_by, self.user)

    def test_replace_project_photo_updates_image_and_classification(self):
        photo = create_project_photo(
            project=self.project,
            image=self._make_image(name="before.jpg", color="blue"),
            classification=PhotoClassification.BEFORE,
            actor=self.user,
            title="Before",
        )

        updated = replace_project_photo(
            photo=photo,
            image=self._make_image(name="final.jpg", color="red"),
            classification=PhotoClassification.FINAL,
            actor=self.user,
            title="Final result",
            description="Completed",
        )

        self.assertEqual(updated.classification, PhotoClassification.FINAL)
        self.assertEqual(updated.original_filename, "final.jpg")
        self.assertEqual(updated.title, "Final result")
        self.assertEqual(updated.description, "Completed")