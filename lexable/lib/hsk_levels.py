import json

from . import unicode_blocks


def get_character_hsk_levels() -> dict[str, int]:
    """Returns a dictionary mapping each character to the HSK level at which it first appears."""
    levels = {}

    for i in range(1, 7):
        with open(f"datasets/hsk_vocab/{i}.json", "r") as fh:
            wordlist = json.load(fh)

        for word in wordlist:
            for c in word["word"]:
                if c in "｜（）〇…":
                    continue

                if unicode_blocks.get_block(c) is not unicode_blocks.UnicodeCodeblocks.CJK_IDEOGRAPHS.value:
                    raise ValueError(f"Unexpected character block in {repr(word["word"])} from HSK level {i}: {unicode_blocks.get_block(c).name}")

                if c not in levels:
                    levels[c] = i

    return levels


def get_level_character_sets() -> dict[int, list[str]]:
    """Returns a dictionary mapping each HSK level to a list of characters first appearing at that level."""
    levels = get_character_hsk_levels()

    out = {}
    for c, level in levels.items():
        if level not in out:
            out[level] = []

        out[level].append(c)

    return out
