import shutil
import tempfile
from decimal import Decimal
from io import BytesIO

from PIL import Image

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.clients.models import Client
from apps.media_assets.models import ProjectPhoto
from apps.projects.models import Project


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class MediaAssetsViewTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="viewuser",
            email="viewuser@example.com",
            password="StrongPass123!",
        )

        cls.customer = Client.objects.create(
            legal_name="View Client",
            commercial_name="View Client",
            client_type="company",
            status="active",
            email="view-client@example.com",
            phone="0777777777",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.customer,
            opportunity=None,
            responsible=cls.user,
            name="View Project",
            description="Testing views",
            location="Cuenca",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

    def _make_image(self, name="upload.jpg"):
        buffer = BytesIO()
        image = Image.new("RGB", (200, 200), color="purple")
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")

    def test_gallery_requires_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("media_assets:project_gallery", kwargs={"project_id": self.project.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_gallery_with_permission_returns_200(self):
        permission = Permission.objects.get(codename="view_project_gallery")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("media_assets:project_gallery", kwargs={"project_id": self.project.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_upload_photo_view_creates_record(self):
        permission = Permission.objects.get(codename="upload_projectphoto")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("media_assets:photo_upload", kwargs={"project_id": self.project.pk}),
            data={
                "image": self._make_image(),
                "classification": "before",
                "title": "Before install",
                "description": "Initial evidence",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProjectPhoto.objects.count(), 1)