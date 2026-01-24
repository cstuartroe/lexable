from django.db import models

from . import user_adds, word


class TrialType(models.TextChoices):
    CITATION_FORM = "citation_form", "citation form"
    DEFINITION = "definition", "definition"
    CLOZE = "cloze", "cloze"
    PRONUNCIATION = "pronunciation", "pronunciation"
    METADATA = "metadata", "metadata"


class Difficulty(models.TextChoices):
    INCORRECT = "incorrect", "incorrect"
    DIFFICULT = "difficult", "difficult"
    MODERATE = "moderate", "moderate"
    EASY = "easy", "easy"


class Trial(models.Model):
    lexeme_add = models.ForeignKey(
        user_adds.LexemeAdd,
        on_delete=models.PROTECT,
        related_name="trials",
    )
    # refers to the local date for user when record was created
    locale_date_created = models.DateField()
    time_created = models.DateTimeField()

    trial_type = models.CharField(choices=TrialType.choices)
    # only set if trial type is cloze
    cloze_word = models.ForeignKey(
        word.WordInSentence,
        on_delete=models.PROTECT,
        related_name="trials",
        null=True,
        blank=True,
    )
    # only set if trial type is metadata
    metadata_field = models.CharField(blank=True)

    # comma-separated choices
    choices = models.CharField()
    difficulty = models.CharField(choices=Difficulty.choices)

