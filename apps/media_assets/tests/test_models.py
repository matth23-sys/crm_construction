import tempfile
import shutil
from io import BytesIO
from decimal import Decimal

from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.clients.models import Client
from apps.media_assets.models import PhotoClassification, ProjectPhoto
from apps.projects.models import Project


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProjectPhotoModelTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="mediauser",
            email="mediauser@example.com",
            password="StrongPass123!",
        )

        cls.customer = Client.objects.create(
            legal_name="Client One",
            commercial_name="Client One",
            client_type="company",
            status="active",
            email="client1@example.com",
            phone="0999999999",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.customer,
            opportunity=None,
            responsible=cls.user,
            name="Roof Project",
            description="Test project",
            location="Quito",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

    def _make_image(self, name="test-photo.jpg"):
        buffer = BytesIO()
        image = Image.new("RGB", (200, 200), color="blue")
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")

    def test_filename_property_returns_basename(self):
        photo = ProjectPhoto.objects.create(
            project=self.project,
            image=self._make_image(),
            classification=PhotoClassification.BEFORE,
            title="Before photo",
            created_by=self.user,
            updated_by=self.user,
        )

        self.assertTrue(photo.filename.endswith(".jpg"))