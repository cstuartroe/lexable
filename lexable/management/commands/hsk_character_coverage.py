import argparse

from django.core.management import base

from lexable.lib import hsk_levels, unicode_blocks
from lexable.models import document as document_lib, sentence as sentence_lib


class Command(base.BaseCommand):
    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-c", "--collection_ids", type=str, required=False,
            help="A comma-separated list of collection ids"
        )

    def handle(self, *args, collection_ids, **options):
        queryset = document_lib.Collection.objects
        if collection_ids:
            collection_ids = [int(n) for n in collection_ids.split(",")]
            queryset = queryset.filter(id__in=collection_ids)

        collections = (
            queryset
            .prefetch_related("documents")
            .prefetch_related("documents__sections")
            .prefetch_related("documents__sections__sentences")
        )

        seen_chars: set[str] = set()
        for collection in collections:
            for document in collection.documents.all():
                for section in document.sections.all():
                    for sentence in section.sentences.all():
                        if sentence.sentence_type in (sentence_lib.SentenceType.HORIZONTAL_RULE.value, sentence_lib.SentenceType.IMAGE.value):
                            continue

                        for c in sentence.text:
                            if unicode_blocks.get_block(c) is unicode_blocks.UnicodeCodeblocks.CJK_IDEOGRAPHS.value:
                                seen_chars.add(c)

        print(f"{len(seen_chars)} total characters seen across the collection set")

        levels = hsk_levels.get_level_character_sets()
        for level, chars in levels.items():
            level_seen_chars = [c for c in chars if c in seen_chars]
            print(f"HSK level {level}: {len(level_seen_chars)}/{len(chars)} seen")
            print(f"Not seen: {''.join([c for c in chars if c not in seen_chars])}")
