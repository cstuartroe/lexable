from dataclasses import dataclass
import enum


@dataclass
class UnicodeCodeblock:
    name: str
    range: tuple[int, int]

    def __hash__(self):
        return hash(self.range)


class UnicodeCodeblocks(enum.Enum):
    BASIC_LATIN = UnicodeCodeblock("Basic Latin", (0x0000, 0x0080))
    LATIN_SUPPLEMENT = UnicodeCodeblock("Latin-1 Supplement", (0x0080, 0x0100))
    GENERAL_PUNCTUATION = UnicodeCodeblock("General Punctuation", (0x2000, 0x2070))
    MATHEMATICAL_OPERATORS = UnicodeCodeblock("Mathematical Operators", (0x2200, 0x2300))
    BOX_DRAWING = UnicodeCodeblock("Box Drawing", (0x2500, 0x2580))
    GEOMETRIC_SHAPES = UnicodeCodeblock("Geometric Shapes", (0x25A0, 0x2600))
    CJK_PUNCTUATION = UnicodeCodeblock("CJK Symbols and Punctuation", (0x3000, 0x3040))
    HIRAGANA = UnicodeCodeblock("Hiragana", (0x3040, 0x30A0))
    CJK_IDEOGRAPHS = UnicodeCodeblock("CJK Unified Ideographs", (0x4E00, 0xA000))
    HALFWITH_AND_FULLWIDTH = UnicodeCodeblock("Halfwidth and Fullwidth Forms", (0xFF00, 0xFFF0))


def get_block(c: str):
    n = ord(c)

    for block in UnicodeCodeblocks:
        start, end = block.value.range

        if start <= n < end:
            return block.value

    raise ValueError(f"Unknown code block for {repr(c)} (position {n:04x})")
