import argparse

from django.core.management import base
from matplotlib import pyplot as plt

from lexable.lib import corpus_stats, hsk_levels, unicode_blocks
from lexable.models import (
    document as document_lib,
    language,
    sentence as sentence_lib,
)


WINDOW = 1000
LOGOGRAM_DENSITY_THRESHOLD = 405
AVG_HSK_LEVEL_THRESHOLD = 2.15


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

        scatter_points = []

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

            logogram_density = corpus_stats.lexical_density(cjk_counts, WINDOW)

            hsk_levels_by_char = hsk_levels.get_character_hsk_levels()
            hsk_level_counts = {}
            for c, count in character_frequencies.items():
                if unicode_blocks.get_block(c) is unicode_blocks.UnicodeCodeblocks.CJK_IDEOGRAPHS.value:
                    # If not in first 6 HSK levels, consider it 8
                    level = hsk_levels_by_char.get(c, 8)

                    hsk_level_counts[level] = hsk_level_counts.get(level, 0) + count
            avg_hsk_numerator = sum(level*count for level, count in hsk_level_counts.items())
            avg_hsk = avg_hsk_numerator/sum(hsk_level_counts.values())

            scatter_points.append((logogram_density, avg_hsk))

            if logogram_density <= LOGOGRAM_DENSITY_THRESHOLD and avg_hsk <= AVG_HSK_LEVEL_THRESHOLD:
                print(collection.title)
                print(f"    Lexable id: {collection.id}")
                print(f"    Link: {collection.link}")
                print(f"    Total length: {sum(character_frequencies.values()):>6}")
                print(f"    Length in CJK characters: {sum(cjk_counts):>6}")
                print(f"    Number of distinct CJK characters: {len(cjk_counts):>4}")
                print(f"    Logogram density (window = {1000}): {logogram_density}")
                print(f"    Average character HSK level: {avg_hsk:.2f}")

        plt.scatter(*zip(*scatter_points))
        plt.show()
