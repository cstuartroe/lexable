from django.db import models

from . import lexeme, sentence


class WordInSentence(models.Model):
    sentence = models.ForeignKey(
        sentence.Sentence,
        on_delete=models.PROTECT,
        related_name="words",
    )
    lexeme_sense = models.ForeignKey(
        lexeme.LexemeSense,
        on_delete=models.PROTECT,
        related_name="words",
    )
    # occasionally, if a word is spelled or used unconventionally, it may not be a good choice to use in cloze trials
    use_in_trials = models.BooleanField()


class Substring(models.Model):
    word = models.ForeignKey(
        WordInSentence,
        on_delete=models.PROTECT,
        related_name="substrings",
    )
    start = models.IntegerField()
    end = models.IntegerField()
