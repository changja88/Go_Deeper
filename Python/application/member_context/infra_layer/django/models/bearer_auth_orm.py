import binascii
import os
from typing import Any

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BearerTokenORM(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    member = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="bearer_token", on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        db_table = "bearer_token"
        verbose_name = "[bearer_token] 토큰 인증 정보"
        verbose_name_plural = "[bearer_token] 토큰 인증 정보"

    def save(self, *args: Any, **kwargs: Any) -> Any:
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls) -> str:
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self) -> Any:
        return self.key
