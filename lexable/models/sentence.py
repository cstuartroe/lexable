from django.db import models

from . import language, document


class SentenceType(models.TextChoices):
    H1 = "h1", "h1"
    H2 = "h2", "h2"
    H3 = "h3", "h3"

    NEW_PARAGRAPH_NO_INDENT = "np", "new paragraph"
    # NEW_PARAGRAPH_INDENT perhaps?
    NEW_PARAGRAPH_BLOCK_INDENT = "npi", "new block-indented paragraph"
    PARAGRAPH_CONTINUED = "p", "paragraph continued"

    HORIZONTAL_RULE = "hr", "horizontal rule"
    IMAGE = "img", "image"


class Sentence(models.Model):
    # If section is null, this sentence is not part of a broader text, but is a separately added one-off entry.
    # The main intention of such one-off sentences is to cover lexeme senses which otherwise have no examples.
    section = models.ForeignKey(
        document.Section,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sentences",
    )
    order = models.IntegerField()
    sentence_type = models.CharField(choices=SentenceType.choices)
    text = models.TextField()
    formatting = models.JSONField()


class SentenceTranslation(models.Model):
    sentence = models.ForeignKey(
        Sentence,
        on_delete=models.PROTECT,
        related_name="translations",
    )
    language = models.TextField(choices=language.LANGUAGE_CHOICES)
    text = models.TextField()
    formatting = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sentence", "language"],
                name="unique_translation_sentence_language",
            ),
        ]

