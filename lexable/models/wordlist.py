from django.db import models

from . import language, lexeme


class WordList(models.Model):
    language = models.CharField(choices=language.LANGUAGE_CHOICES)
    # Currently, wordlist titles are untranslated; this makes user-generated wordlists easier to implement, but
    # might change in the future.
    title = models.CharField()


class WordListItem(models.Model):
    wordlist = models.ForeignKey(
        WordList,
        on_delete=models.PROTECT,
        related_name="items",
    )
    order = models.IntegerField()
    lexeme = models.ForeignKey(
        lexeme.Lexeme,
        on_delete=models.PROTECT,
        related_name="wordlist_inclusions",
    )
