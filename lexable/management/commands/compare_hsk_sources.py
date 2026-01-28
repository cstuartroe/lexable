import argparse

from django.core.management import base


from lexable.lib import hsk


class Command(base.BaseCommand):
    help = (
        "The Chinese government intends to adhere to a different syllabus beginning July 2026. "
        "mandarinbean.com has the old HSK 3.0 syllabus."
    )

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def handle(self, *args, **options):
        official_vocab = hsk.vocab_by_level(hsk.OFFICIAL)
        mb_vocab = hsk.vocab_by_level(hsk.MANDARINBEAN)

        official_chars = hsk.get_level_character_sets(hsk.OFFICIAL)
        mb_chars = hsk.get_level_character_sets(hsk.MANDARINBEAN)

        for level in hsk.LEVELS:
            print(f"Level {level}:")
            print(f"    official has {len(official_vocab[level]):>4} words, {len(official_chars[level]):>4} chars")
            print(f"    mb       has {len(mb_vocab[level]):>4} words, {len(mb_chars[level]):>4} chars")
