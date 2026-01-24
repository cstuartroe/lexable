from enum import Enum


# ISO 639-3 language codes, in alphabetical order
class Language(Enum):
    Arabic = "arb" # Standard Arabic sub-code of ara Arabic
    Mandarin = "cmn" # Mandarin sub-code of zho Chinese
    German = "deu"
    English = "eng"
    Esperanto = "epo"
    French = "fra"
    Hebrew = "heb"
    Hindi = "hin"
    Italian = "ita"
    Japanese = "jpn"
    Korean = "kor"
    Dutch = "nld"
    Portuguese = "por"
    Russian = "rus"
    Spanish = "spa"
    Turkish = "tur"


LANGUAGE_CHOICES = [
    (l.value, l.name)
    for l in Language
]
