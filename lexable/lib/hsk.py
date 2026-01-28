from dataclasses import dataclass
import json

from . import unicode_blocks


OFFICIAL = "official"
MANDARINBEAN = "mandarinbean"

DEFAULT_SOURCE = OFFICIAL

LEVELS = ["1", "2", "3", "4", "5", "6", "7-9"]


@dataclass
class HSKVocab:
    word: str
    pinyin: str
    definition: str | None
    level: str
    pos: str | None


def load_vocab(source: str = DEFAULT_SOURCE) -> list[HSKVocab]:
    with open(f"datasets/hsk_vocab/{source}.json", "r") as fh:
        wordlist = json.load(fh)

    return [
        HSKVocab(**word)
        for word in wordlist
    ]


def vocab_by_level(source: str = DEFAULT_SOURCE) -> dict[str, list[HSKVocab]]:
    out = {
        level: []
        for level in LEVELS
    }

    for word in load_vocab(source):
        out[word.level].append(word)

    return out


def get_character_hsk_levels(source: str = DEFAULT_SOURCE) -> dict[str, str]:
    """Returns a dictionary mapping each character to the HSK level at which it first appears."""
    levels = {}

    words = load_vocab(source)

    for word in words:
        for c in word.word:
            if c in "｜（）〇…":
                continue

            if unicode_blocks.get_block(c) is not unicode_blocks.UnicodeCodeblocks.CJK_IDEOGRAPHS.value:
                raise ValueError(f"Unexpected character block in {repr(word["word"])}: {unicode_blocks.get_block(c).name}")

            if c not in levels:
                levels[c] = word.level

    return levels


def get_level_character_sets(source: str = DEFAULT_SOURCE) -> dict[str, list[str]]:
    """Returns a dictionary mapping each HSK level to a list of characters first appearing at that level."""
    levels = get_character_hsk_levels(source)

    out = {
        level: []
        for level in LEVELS
    }
    for c, level in levels.items():
        out[level].append(c)

    return out
