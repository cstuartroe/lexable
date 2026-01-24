from django.db import models
from django.contrib.auth import models as auth_models

from . import lexeme as lexeme_model, document


class LexemeAdd(models.Model):
    """LexemeAdd represents a lexeme being added to a user's flashcards *or* being marked as not reviewable.

    Once a lexeme has appeared twice in the material marked as read by the user, if its add_by_default field is True,
    a LexemeAdd is created.
    Alternatively, a user may manually mark any lexeme as added, creating a LexemeAdd.
    locale_date_created and time_created refer to this creation event.
    The user may later mark a lexeme as excluded (or, thereafter, included again) from their flashcard deck,
    which will set in_flashcards accordingly, and update time_updated.
    """

    lexeme = models.ForeignKey(
        lexeme_model.Lexeme,
        on_delete=models.PROTECT,
        related_name="lexeme_adds",
    )
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="lexeme_adds",
    )

    # in_flashcards is initially set to True
    in_flashcards = models.BooleanField()

    # refers to the local date for user when record was created
    locale_date_created = models.DateField()
    time_created = models.DateTimeField()
    # set to when the record was created, or when in_flashcards was most recently changed
    time_updated = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lexeme", "user"],
                name="unique_add_lexeme_user",
            ),
        ]


class SectionAdd(models.Model):
    """SectionAdd represents a section being marked as read by a user.
    """

    section = models.ForeignKey(
        document.Section,
        on_delete=models.PROTECT,
        related_name="section_adds",
    )
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="section_adds",
    )

    # refers to the local time for the user when the section was marked read
    locale_day_created = models.DateField()
    time_created = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "user"],
                name="unique_add_section_user",
            ),
        ]
