#!/usr/bin/env python3
"""Find words used in the 1830 Book of Mormon that don't appear in Webster's 1828 dictionary."""

import json
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DICTIONARY_PATH = REPO_ROOT / "data" / "websters_1828_words.txt"
BOM_DIR = REPO_ROOT / "data" / "bom_1830"
OUTPUT_PATH = REPO_ROOT / "output" / "unique_bom_words.txt"

WORD_RE = re.compile(r"[A-Za-z']+")


def load_dictionary_words() -> set[str]:
    with DICTIONARY_PATH.open(encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def iter_bom_words():
    for json_path in sorted(BOM_DIR.rglob("*.json")):
        with json_path.open(encoding="utf-8") as f:
            chapter = json.load(f)
        for verse in chapter["verses"]:
            for match in WORD_RE.finditer(verse["text"]):
                word = match.group().strip("'")
                if word:
                    yield word.lower()


def main() -> None:
    dictionary_words = load_dictionary_words()
    bom_word_counts = Counter(iter_bom_words())

    unique_words = {
        word: count
        for word, count in bom_word_counts.items()
        if word not in dictionary_words
    }

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for word in sorted(unique_words):
            f.write(f"{word}\t{unique_words[word]}\n")

    print(f"Dictionary words: {len(dictionary_words)}")
    print(f"Distinct BoM words: {len(bom_word_counts)}")
    print(f"Unique BoM words (not in dictionary): {len(unique_words)}")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
