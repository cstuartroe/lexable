from django.contrib import admin

from lexable.models import derived, document, lexeme, purchases, sentence, trial, user_adds, user_settings, word, wordlist


admin.site.register(derived.LexemeForm)
admin.site.register(derived.UserHistoryDate)
admin.site.register(derived.CardDueDate)
admin.site.register(derived.CreditBalance)

admin.site.register(document.Collection)
admin.site.register(document.CollectionTitleTranslation)
admin.site.register(document.Document)
admin.site.register(document.DocumentTitleTranslation)
admin.site.register(document.Section)

admin.site.register(lexeme.Lexeme)
admin.site.register(lexeme.Etymology)
admin.site.register(lexeme.LexemeSense)
admin.site.register(lexeme.Definition)

admin.site.register(purchases.CreditPurchase)
admin.site.register(purchases.DocumentUnlock)

admin.site.register(sentence.Sentence)
admin.site.register(sentence.SentenceTranslation)

admin.site.register(trial.Trial)

admin.site.register(user_adds.LexemeAdd)
admin.site.register(user_adds.SectionAdd)

admin.site.register(user_settings.UserSettings)

admin.site.register(word.WordInSentence)
admin.site.register(word.Substring)

admin.site.register(wordlist.WordList)
admin.site.register(wordlist.WordListItem)
