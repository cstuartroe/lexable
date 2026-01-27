import argparse

from django.core.management import base
from django.db import transaction

from lexable.lib.content_downloads import jjwxc


class Command(base.BaseCommand):
    help = "Downloads a collection from jjwxc.net"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("novel_id", type=int)
        parser.add_argument("chapter_range", type=str)

    @transaction.atomic
    def handle(self, *args, novel_id, chapter_range, **options):
        start, end = chapter_range.split("-")

        jjwxc.download_jjwxc(novel_id, (int(start), int(end)))
