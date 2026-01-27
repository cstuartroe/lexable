import argparse
import codecs

import bs4
from django.core.management import base
from django.db import transaction
import requests

from lexable.models import document, language, sentence


def download_jjwxc(novel_id: int, chapter_range: tuple[int, int], title: str | None = None):
    """Downloads a story from jjwxc.net

    :argument novel_id: Numerical id of novel, visible as a get param in the jjwxc.net URL.
    :argument chapter_range: Inclusive by 1-indexed chapter numbers visible on the site, not a typical Python range.
    :argument title: Optional, override of title. Most useful for jjwxc.net stories that consist of multiple volumes,
        to rename the individual volumes.
    """

    url = f"https://www.jjwxc.net/onebook.php?novelid={novel_id}"
    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.content, features="html.parser")

    image = soup.find("img", {"itemprop": "image"})["src"]
    description = soup.find("div", {"itemprop": "description"}).text.strip()

    chapter_table = soup.find("table", {"id": "oneboolt"})

    if title is None:
        title = chapter_table.tr.find("h1", {"itemprop": "name"}).text.strip()
    author = chapter_table.tr.find("span", {"itemprop": "author"}).text.strip()

    collection = document.Collection(
        language=language.Language.Mandarin.value,
        title=title,
        author=author,
        description=description,
        link=url,
        image=image,
        published=False,
        free=False,
    )
    collection.save()

    chapters = [
        row
        for row in chapter_table.find_all("tr")
        if "chapter" in row.get("itemprop", "").split()
    ]

    for i, chapter in enumerate(chapters):
        if str(i + 1) != chapter.td.text.strip():
            print(f"At {url}, unexpected content of left column: want = {i+1}, got = {repr(chapter.td.text.strip())}")
            break

    start, end = chapter_range
    selected_chapters = chapters[start - 1:end]
    for i, chapter in enumerate(selected_chapters):
        chapter_url = chapter.find("a", {"itemprop": "url"})["href"]
        res = requests.get(chapter_url)

        text = codecs.decode(res.content, encoding="gb18030", errors="ignore")

        soup = bs4.BeautifulSoup(text, features="html.parser")

        chapter_record = document.Document(
            collection=collection,
            order=i + 1,
            title=soup.h2.text.strip(),
        )
        chapter_record.save()

        element = soup.h2.parent.next_sibling
        while element.text.strip() == "":
            element = element.next_sibling

        sentences_by_section = [[]]
        last_was_br = False
        while element is not None:
            if isinstance(element, bs4.element.Tag):
                if element.name == "br":
                    if last_was_br:
                        sentences_by_section.append([])
                    else:
                        last_was_br = True
                elif element.name == "div" and element.attrs["id"] == "favoriteshow_3":
                    break
                else:
                    raise ValueError(F"Unexpected tag: {element}")

            elif isinstance(element, bs4.element.NavigableString):
                sentences_by_section[-1].append(element.text.strip())
                last_was_br = False

            else:
                raise ValueError("Unknown node type")

            element = element.next_sibling

        for j, sentences in enumerate(sentences_by_section):
            section = document.Section(
                document=chapter_record,
                order=j + 1,
            )
            section.save()

            for k, sentence_str in enumerate(sentences):
                sentence_record = sentence.Sentence(
                    section=section,
                    order=k + 1,
                    sentence_type=sentence.SentenceType.NEW_PARAGRAPH_NO_INDENT,
                    text=sentence_str,
                    formatting={},
                )
                sentence_record.save()