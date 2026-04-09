"""
Modelos base abstractos para todo el proyecto.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("creado en", default=timezone.now, editable=False, db_index=True)
    updated_at = models.DateTimeField("actualizado en", auto_now=True, db_index=True)
    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created", verbose_name="creado por", editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_updated", verbose_name="actualizado por")
    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField("eliminado", default=False, db_index=True)
    deleted_at = models.DateTimeField("eliminado en", null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_deleted", verbose_name="eliminado por")
    class Meta:
        abstract = True
    
    def soft_delete(self, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])
    
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])


class BaseModel(UUIDModel, TimeStampedModel, UserStampedModel, SoftDeleteModel):
    class Meta:
        abstract = True


class BaseModelWithoutSoftDelete(UUIDModel, TimeStampedModel, UserStampedModel):
    class Meta:
        abstract = True
