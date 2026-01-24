from django.db import models
from django.contrib.auth import models as auth_models

from . import language


class UserSettings(models.Model):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="user_settings",
    )
    learning_from = models.CharField(choices=language.LANGUAGE_CHOICES)
    currently_learning = models.CharField(choices=language.LANGUAGE_CHOICES)
    ask_difficulty = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="unique_user_settings",
            ),
        ]
