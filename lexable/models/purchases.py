from django.db import models
from django.contrib.auth import models as auth_models

from . import document


STARTING_CREDIT_BALANCE: int = 10


class CreditPurchase(models.Model):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="credit_purchases",
    )
    credits = models.IntegerField()
    time_created = models.DateTimeField()


class DocumentUnlock(models.Model):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="document_unlocks",
    )
    document = models.ForeignKey(
        document.Document,
        on_delete=models.PROTECT,
        related_name="unlocks",
    )
    time_created = models.DateTimeField()
