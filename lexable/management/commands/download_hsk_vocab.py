from django.core.management import base

from lexable.lib.content_downloads import hsk_vocab


class Command(base.BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # hsk_vocab.download_mandarinbean()
        hsk_vocab.parse_official()
