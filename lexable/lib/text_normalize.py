import re


def normalize(text: str):
    return re.sub(
        " +",
        " ",
        text
        .replace("\t", " ")
        .replace("\xa0", " ")  # No-break space
        .strip()
    )
