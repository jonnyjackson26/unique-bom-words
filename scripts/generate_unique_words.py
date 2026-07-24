#!/usr/bin/env python3
"""Find words used in the 1830 Book of Mormon that don't appear in Webster's 1828 dictionary."""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DICTIONARY_PATH = REPO_ROOT / "data" / "websters_1828_words.txt"
BOM_DIR = REPO_ROOT / "data" / "bom_1830"
WORDS_OUTPUT_PATH = REPO_ROOT / "output" / "unique_bom_words.txt"
REFERENCES_OUTPUT_PATH = REPO_ROOT / "output" / "unique_bom_words_references.tsv"

# A "word" is a maximal run of Latin letters, plus straight (') and curly (’)
# apostrophes -- which are then stripped out entirely rather than treated as a
# boundary, so "Lord's" / "Lord’s" both become "lords", not two tokens or a
# literal apostrophe in the output. See README.md's "What counts as a word"
# section for the full definition, including why hyphens *do* split words.
WORD_RE = re.compile(r"[A-Za-z'’]+")

# Canonical Book of Mormon book order, matching the folder names under data/bom_1830.
BOOK_ORDER = [
    "1-nephi", "2-nephi", "jacob", "enos", "jarom", "omni", "words-of-mormon",
    "mosiah", "alma", "helaman", "3-nephi", "4-nephi", "mormon", "ether", "moroni",
]


def load_dictionary_words() -> set[str]:
    with DICTIONARY_PATH.open(encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def iter_chapter_files():
    for book_folder in BOOK_ORDER:
        chapter_files = (BOM_DIR / book_folder).glob("*.json")
        for path in sorted(chapter_files, key=lambda p: int(p.stem)):
            yield path


def iter_bom_word_references():
    """Yield (lowercase_word, "Book Chapter:Verse") for every word token in the text."""
    for json_path in iter_chapter_files():
        with json_path.open(encoding="utf-8") as f:
            chapter = json.load(f)
        book, chapter_num = chapter["book"], chapter["chapter"]
        for verse in chapter["verses"]:
            reference = f"{book} {chapter_num}:{verse['verse']}"
            for match in WORD_RE.finditer(verse["text"]):
                word = match.group().replace("'", "").replace("’", "")
                if word:
                    yield word.lower(), reference


def main() -> None:
    dictionary_words = load_dictionary_words()

    bom_word_counts: Counter[str] = Counter()
    references_by_word: dict[str, list[str]] = defaultdict(list)
    for word, reference in iter_bom_word_references():
        bom_word_counts[word] += 1
        references_by_word[word].append(reference)

    unique_words = sorted(
        word for word in bom_word_counts if word not in dictionary_words
    )

    WORDS_OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with WORDS_OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for word in unique_words:
            f.write(f"{word}\t{bom_word_counts[word]}\n")

    with REFERENCES_OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write("word\treference\n")
        for word in unique_words:
            for reference in references_by_word[word]:
                f.write(f"{word}\t{reference}\n")

    print(f"Dictionary words: {len(dictionary_words)}")
    print(f"Distinct BoM words: {len(bom_word_counts)}")
    print(f"Unique BoM words (not in dictionary): {len(unique_words)}")
    print(f"Wrote {WORDS_OUTPUT_PATH}")
    print(f"Wrote {REFERENCES_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
