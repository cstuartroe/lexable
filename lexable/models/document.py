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

    def to_json(self, with_documents: bool):
        data = {
            "id": self.id,
            "language": self.language,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "link": self.link,
            "image": self.image,
            "published": self.published,
            "free": self.free,
        }

        if with_documents:
            data["documents"] = [
                d.to_json(with_content=False)
                for d in sorted(
                    self.documents.all(),
                    key=lambda document: document.order,
                )
            ]

        return data


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
    link = models.CharField()

    def to_json(self, with_content: bool):
        data = {
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "collection": self.collection.to_json(with_documents=False),
        }
        if with_content:
            data["sections"] = [
                s.to_json()
                for s in sorted(
                    self.sections.all(),
                    key=lambda section: section.order,
                )
            ]
        return data


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

    def to_json(self):
        return {
            "id": self.id,
            "sentences": [
                s.to_json()
                for s in sorted(
                    self.sentences.all(),
                    key=lambda sentence: sentence.order,
                )
            ],
        }
