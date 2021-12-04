"""
Tokenize string considering the white spaces and punctuation.
@see https://stackoverflow.com/questions/6162600/how-do-you-split-a-javascript-string-by-spaces-and-punctuation
"""

import re
from typing import Iterable

NEWLINE_PLACEHOLDER = "§"
PARAGRAPH_CHARACTER = "\n\n"

punctuation = "\\" + "\\".join(list("[](){}!?.,:;'\"\\/*&^%$_+-–—=<>@|~"))
ellipsis = "\\.{3}"

words = "[a-zA-Zа-яА-ЯёЁ]+"
compounds = f"{words}-{words}"

newlines_re = re.compile(r"\n\s*")
tokenize_re = re.compile(f"({ellipsis}|{compounds}|{words}|[{punctuation}])")


def tokenize(text: str) -> list[str]:
    paragraphed = newlines_re.sub(NEWLINE_PLACEHOLDER, text)
    return [token for token in tokenize_re.split(paragraphed) if token]


def textify(tokens: Iterable[str]) -> str:
    nonempty = filter(bool, tokens)
    return "".join(nonempty).replace(NEWLINE_PLACEHOLDER, PARAGRAPH_CHARACTER)
