"""
This file contains models which are not considered sources of truth, but which are entirely derived from the
information contained in other models.

They are used to index information, and thereby speed up queries, but it is in principle safe to delete all entries in
these tables, in the sense that information would not in such case be destroyed.
If this were to happen, all entries in the tables would need to be re-computed, and disruption to users would
nevertheless occur in the meantime.

For each table in this file, the normal application logic should populate them as needed. Management commands should
also be written which create/delete/alter records in each of the tables to resolve data inconsistency or reflect changes
to how the content of the tables is derived.
"""

from django.db import models
from django.contrib.auth import models as auth_models

from . import lexeme as lexeme_model, language as language_model, user_adds, trial


class LexemeForm(models.Model):
    """LexemeForm represents a particular surface form, e.g., "liked", of a lexeme, e.g. "to like".

    It keeps track of how many word.WordInSentence records represent a given orthographic form of a lexeme.
    It is used mainly for lexeme search when annotating.
    For word.WordInSentence records with multiple substrings, the substrings are simply joined in order with a space.
    """
    form = models.CharField()
    lexeme = models.ForeignKey(
        lexeme_model.Lexeme,
        on_delete=models.PROTECT,
        related_name="forms",
    )

    # language must be equal to lexeme.language
    language = models.CharField(choices=language_model.LANGUAGE_CHOICES)
    num_occurrences = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["form", "lexeme"],
                name="unique_lexeme_form",
            ),
        ]


class UserHistoryDate(models.Model):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="history_dates",
    )
    date = models.DateField()
    language = models.CharField(choices=language_model.LANGUAGE_CHOICES)

    words_read = models.IntegerField()
    lexemes_added = models.IntegerField()
    cards_played = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date", "language"],
                name="unique_user_history_date",
            ),
        ]


class CardDueDate(models.Model):
    lexeme_add = models.ForeignKey(
        user_adds.LexemeAdd,
        on_delete=models.PROTECT,
        related_name="due_dates",
    )
    trial_type = models.CharField(choices=trial.TrialType.choices)
    # sense is non-null iff trial_type is definition
    sense = models.ForeignKey(
        lexeme_model.LexemeSense,
        on_delete=models.PROTECT,
        related_name="due_dates",
        null=True,
    )

    metadata_field = models.CharField()
    due_date = models.DateField()
    last_reviewed = models.DateField(null=True)

    # Constraints:
    # - if trial_type is definition, sense is non-null and record is unique for lexeme_add, trial_type, sense triplet
    # - otherwise, sense is null and record is unique for lexeme_add, trial_type pair
    # This is not easily expressible using Django constraints and this is a derived table that can always be
    # corrected, so no constraint is defined here.


class CreditBalance(models.Model):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.PROTECT,
        related_name="credit_balance",
    )

    balance = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="unique_credit_balance_user",
            ),
        ]
