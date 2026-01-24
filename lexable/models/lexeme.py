from django.db import models
from django.contrib.auth import models as auth_models

from . import language


class Lexeme(models.Model):
    language = models.CharField(choices=language.LANGUAGE_CHOICES)
    # part of speech is an open text field at the model level;
    # parts of speech are defined per language and enforced elsewhere.
    part_of_speech = models.CharField()
    citation_form = models.CharField()
    pronunciation = models.CharField()
    # metadata may encompass any grammatical information: gender, unpredictable inflections, etc.
    metadata = models.JSONField()
    # an href to some mnemonic image; optional
    image = models.CharField(blank=True)
    # owner is the user who created/owns the dictionary entry
    owner = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="owned_lexemes",
    )
    add_by_default = models.BooleanField()


class EtymologyType(models.TextChoices):
    DERIVED = "derived", "derived"  # derived via morphology
    CONTAINS = "contains", "contains"  # of a phrase, containing a word
    VARIANT = "variant", "variant"  # a spelling and/or pronunciation variant with no difference in meaning


class Etymology(models.Model):
    """A many-to-many accounting of lexemes containing or being derived from other lexemes.
    """
    source_lexeme = models.ForeignKey(
        Lexeme,
        on_delete=models.PROTECT,
        related_name="derivations",
    )
    derived_lexeme = models.ForeignKey(
        Lexeme,
        on_delete=models.PROTECT,
        related_name="etymologies",
    )
    etymology_type = models.CharField(choices=EtymologyType.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_lexeme", "derived_lexeme"],
                name="unique_etymology",
            ),
        ]


class LexemeSense(models.Model):
    lexeme = models.ForeignKey(
        Lexeme,
        on_delete=models.PROTECT,
        related_name="senses",
    )


class Definition(models.Model):
    sense = models.ForeignKey(
        LexemeSense,
        on_delete=models.PROTECT,
        related_name="definitions",
    )
    language = models.CharField(choices=language.LANGUAGE_CHOICES)
    text = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sense", "language"],
                name="unique_definition_sense_language",
            ),
        ]
