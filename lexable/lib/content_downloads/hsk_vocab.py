import json
import re

import bs4
import requests

from lexable.lib import text_normalize, unicode_blocks


def download_mandarinbean_wordlist(n: int):
    url = f"https://mandarinbean.com/new-hsk-{n}-word-list/"
    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.content, features="html.parser")

    data = []

    char_table = soup.find("table", {"class": "has-subtle-pale-blue-background-color has-background"})
    for row in char_table.tbody.find_all("tr"):
        cells = row.find_all("td")

        word = cells[1].text
        word = text_normalize.normalize(word)
        word = re.sub("（.*）$", "", word)
        word = word.replace("¹", "").replace("²", "")

        data.append({
            "word": word,
            "pinyin": text_normalize.normalize(cells[2].text),
            "definition": text_normalize.normalize(cells[3].text.replace("\n", " ")),
            "level": str(n),
            "pos": None,
        })

    return data


def download_mandarinbean():
    data = []
    for i in range(1, 7):
        data += download_mandarinbean_wordlist(i)

    with open("datasets/hsk_vocab/mandarinbean.json", "w") as fh:
        json.dump(
            data,
            fh,
            indent=2,
            ensure_ascii=False,
        )


VOCAB_LINE_RE = r"(\d{1,5}) ([1-9（）-]+) ([^a-z]{1,12}) ([a-züāáǎàēéěèīíǐìōóǒòūúǔùǚǜǹ ’/-]+)( ([^a-z]+))?\n"


def separate_levels(level: str, pos: str):
    if "（" in level:
        lower_levels, upper_level = re.fullmatch("(.+)（(.+)）", level).groups()
        lower_poss, upper_pos = re.fullmatch("(.+)、（(.+)）", pos).groups()

        yield from separate_levels(lower_levels, lower_poss)
        yield upper_level, upper_pos
    else:
        yield level, pos


def parse_official():
    """Parses datasets/hsk_vocab/新版HSK考试大纲1219.txt, which is the text data extracted from
    https://hsk.cn-bj.ufileos.com/3.0/%E6%96%B0%E7%89%88HSK%E8%80%83%E8%AF%95%E5%A4%A7%E7%BA%B21219.pdf,
    a document published by the Chinese government.
    """

    with open("datasets/hsk_vocab/新版HSK考试大纲1219.txt", "r") as fh:
        lines = fh.readlines()

    vocab_lines = [
        (line, re.fullmatch(VOCAB_LINE_RE, line, flags=re.IGNORECASE))
        for line in lines
        if re.fullmatch(VOCAB_LINE_RE, line, flags=re.IGNORECASE)
    ]

    vocab_by_number = {}

    for _, match in vocab_lines:
        number, level, word, pinyin, _, pos = match.groups()

        if pos is not None:
            pos = pos.replace(" ", "")

        assert number not in vocab_by_number

        if word[-1] in "12":
            word = word[:-1]
        for c in word:
            if unicode_blocks.get_block(c) is not unicode_blocks.UnicodeCodeblocks.CJK_IDEOGRAPHS.value:
                raise ValueError(f"Word {number} contains non-CJK characters: {word}")

        vocab_by_number[number] = {
            "word": word,
            "pinyin": pinyin,
            "definition": None,
            "level": level,
            "pos": pos,
        }

    vocab_list = []
    for i in range(1, 11001):
        if str(i) in vocab_by_number:
            raw_vocab = vocab_by_number[str(i)]

            levels = list(separate_levels(raw_vocab["level"], raw_vocab["pos"]))
            if len(levels) > 1:
                print(f"Word {raw_vocab["word"]} has {len(levels)} levels: {levels}")

            for level, pos in levels:
                vocab_list.append({
                    **raw_vocab,
                    "level": level,
                    "pos": pos,
                })

        else:
            print(f"Missing number {i}")

    with open("datasets/hsk_vocab/official.json", "w") as fh:
        json.dump(
            vocab_list,
            fh,
            indent=2,
            ensure_ascii=False,
        )
