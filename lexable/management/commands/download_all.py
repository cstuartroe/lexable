import argparse

from django.core.management import base
from django.db import transaction
import tqdm

from lexable.lib.content_downloads import jjwxc


DOCS = [
    # Sections of 水心沙's 宝珠鬼话
    (128864, (1, 8), "宝珠鬼话：锁麒麟"),
    (128864, (9, 20), "宝珠鬼话：影蜃"),
    (128864, (21, 33), "宝珠鬼话：阴亲"),
    (128864, (34, 54), "宝珠鬼话：野蔷薇"),
    (128864, (55, 70), "宝珠鬼话：丧鬼"),
    (128864, (71, 80), "宝珠鬼话：术士"),
    (128864, (81, 99), "宝珠鬼话：镇魂钉"),
    (128864, (100, 113), "宝珠鬼话：灰姑娘"),
    (128864, (114, 125), "宝珠鬼话：还魂香"),
    # Top stories in 言情 section
    (330249, (1, 12), None),
    (1722284, (1, 39), None),
    (3076116, (1, 17), None),
    (7707127, (1, 15), None),
    # Top stories in 原创 section
    (582026, (1, 20), None),
    (2070505, (1, 20), None),
    (1737310, (1, 30), None),
    (1248812, (1, 24), None),
    # Stories recommended by https://heavenlypath.notion.site/Webnovels-Books-29ee006777bd4d9fbbd0ea5eb29ec514
    (4062436, (1, 4), None),
    (5033642, (1, 23), None),
    (4555084, (1, 2), None),
    (2048550, (1, 7), None),
    (4411966, (1, 23), None),
]


class Command(base.BaseCommand):
    help = "Downloads a set of known collections"

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        for novel_id, chapter_range, title in tqdm.tqdm(DOCS):
            jjwxc.download_jjwxc(novel_id, chapter_range, title)
