import uuid

from django.db import models
from django.urls import reverse

from shapeblock.utils.models import BaseModel, OwnedModel

from fernet_fields import EncryptedCharField


class CloudProvider(BaseModel, OwnedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(null=False, max_length=50)

    CLOUD_CHOICES = (
        ("digitalocean", "Digitalocean"),
        ("linode", "Linode"),
        ("aws", "AWS"),
    )
    cloud = models.CharField(max_length=20, blank=True, choices=CLOUD_CHOICES)

    def __str__(self):
        return f"{self.name}({self.cloud})"

    def get_absolute_url(self):
        return reverse("providers:detail", args=[self.uuid])


class Digitalocean(CloudProvider):
    api_key = EncryptedCharField(null=False, max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cloud = "digitalocean"
        super().save(*args, **kwargs)


class Linode(CloudProvider):
    token = EncryptedCharField(null=False, max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cloud = "linode"
        super().save(*args, **kwargs)


class AWS(CloudProvider):
    access_key = EncryptedCharField(null=False, max_length=100)
    secret_key = EncryptedCharField(null=False, max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.cloud = "aws"
        super().save(*args, **kwargs)
