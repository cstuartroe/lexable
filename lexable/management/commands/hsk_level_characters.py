from django.core.management import base

from lexable.lib import hsk


class Command(base.BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        levels = hsk_levels.get_character_hsk_levels()

        count_per_level = {}
        for _, level in levels.items():
            count_per_level[level] = count_per_level.get(level, 0) + 1

        for level in sorted(set(levels.values())):
            print(f"HSK level {level}: {count_per_level[level]:>4} characters")
