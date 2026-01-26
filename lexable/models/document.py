from django.db import models

from . import language


class Collection(models.Model):
    language = models.CharField(choices=language.LANGUAGE_CHOICES)
    title = models.CharField()
    author = models.CharField()
    description = models.TextField()
    link = models.CharField()
    image = models.CharField()
    published = models.BooleanField()
    free = models.BooleanField()


class CollectionTitleTranslation(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="title_translations",
    )
    language = models.CharField(choices=language.LANGUAGE_CHOICES)
    title = models.CharField()
    description = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["collection", "language"],
                name="unique_title_translation_collection_language",
            ),
        ]


class Document(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="documents",
    )
    order = models.IntegerField()
    title = models.CharField()


class DocumentTitleTranslation(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
        related_name="title_translations",
    )
    language = models.CharField(choices=language.LANGUAGE_CHOICES)
    title = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "language"],
                name="unique_title_translation_document_language",
            ),
        ]


class Section(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
        related_name="sections",
    )
    order = models.IntegerField()
