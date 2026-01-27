import json

from . import unicode_blocks


def get_character_hsk_levels():
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
