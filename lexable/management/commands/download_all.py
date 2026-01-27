import argparse

from django.core.management import base
from django.db import transaction
import tqdm

from lexable.lib.content_downloads import jjwxc


JJWXC_COLLECTIONS = [
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
    (271008, (1, 18), None),
    (2419670, (1, 22), None),
    (8877874, (1, 18), None),
    (2967663, (1, 17), None),
    (2013355, (1, 30), None),
    (4177857, (1, 16), None),
    (6806636, (1, 12), None),
    (1675838, (1, 12), None),
    # Top stories in 原创 section
    (582026, (1, 20), None),
    (2070505, (1, 20), None),
    (1737310, (1, 30), None),
    (1248812, (1, 24), None),
    (1673146, (1, 24), None),
    (4693139, (1, 19), None),
    (5337159, (1, 14), None),
    (789815, (1, 21), None),
    (8217200, (1, 18), None),
    (3278715, (1, 16), None),
    (209155, (1, 8), None),
    # Top stories in 无CP+小说 section
    (2792058, (1, 24), None),
    (2213711, (1, 3), None),
    (2374010, (1, 27), None),
    (4506678, (1, 21), None),
    (1180294, (1, 26), None),
    (2368775, (1, 32), None),
    (2042413, (1, 44), None),
    (1988155, (1, 24), None),
    (3695116, (1, 21), None),
    (6617563, (1, 16), None),
    (3190350, (1, 22), None),
    # Stories recommended by https://heavenlypath.notion.site/Webnovels-Books-29ee006777bd4d9fbbd0ea5eb29ec514
    (4062436, (1, 4), None),
    (5033642, (1, 23), None),
    (4555084, (1, 2), None),
    (2048550, (1, 7), None),
    (4411966, (1, 23), None),
    (3967930, (1, 17), None),
    (4419265, (1, 23), None),
]


class Command(base.BaseCommand):
    help = "Downloads a set of known collections"

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        for novel_id, chapter_range, title in tqdm.tqdm(JJWXC_COLLECTIONS):
            jjwxc.download_jjwxc(novel_id, chapter_range, title)
