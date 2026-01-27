import json
import re

import bs4
import requests

from lexable.lib import text_normalize


def download_wordlist(n: int):
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
        })

    with open(f"datasets/hsk_vocab/{n}.json", "w") as fh:
        json.dump(data, fh, indent=2)


def download_all():
    for i in range(1, 7):
        download_wordlist(i)
