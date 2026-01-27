import argparse

from django.core.management import base

from lexable.lib import corpus_stats, unicode_blocks
from lexable.models import (
    document as document_lib,
    language,
    sentence as sentence_lib,
)


WINDOW = 1000


class Command(base.BaseCommand):
    help = "Analyzes lexeme density of collections"

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def handle(self, *args, **options):
        mandarin_collections = list(
            document_lib.Collection.objects
            .prefetch_related("documents")
            .prefetch_related("documents__sections")
            .prefetch_related("documents__sections__sentences")
            .filter(language=language.Language.Mandarin.value)
        )

        for collection in mandarin_collections:
            character_frequencies = {}
            block_frequencies = {}

            for document in collection.documents.all():
                for section in document.sections.all():
                    for sentence in section.sentences.all():
                        if sentence.sentence_type in (sentence_lib.SentenceType.HORIZONTAL_RULE, sentence_lib.SentenceType.IMAGE):
                            continue

                        for c in sentence.text:
                            character_frequencies[c] = character_frequencies.get(c, 0) + 1

                            block = unicode_blocks.get_block(c)
                            block_frequencies[block] = block_frequencies.get(block, 0) + 1

            block_diversity = {}
            for c in character_frequencies.keys():
                block = unicode_blocks.get_block(c)
                block_diversity[block] = block_diversity.get(block, 0) + 1

            cjk_counts = [
                count
                for c, count in character_frequencies.items()
                if unicode_blocks.get_block(c) is unicode_blocks.UnicodeCodeblocks.CJK_IDEOGRAPHS.value
            ]

            print(collection.title)
            print(f"    Total length: {sum(character_frequencies.values()):>6}")
            print(f"    Length in CJK characters: {sum(cjk_counts):>6}")
            print(f"    Number of distinct CJK characters: {len(cjk_counts):>4}")
            print(f"    Logogram density (window = {1000}): {corpus_stats.lexical_density(cjk_counts, WINDOW)}")
