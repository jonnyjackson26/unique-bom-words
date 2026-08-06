#!/usr/bin/env python3
"""Generate output/categories/<category>.md from output/curated_bom_words.csv.

Each category file is a bullet list, one line per word in that category:
    - word (count) - REFS

REFS shows at most the first 2 verse references (in canonical book order);
if the word occurs more than twice, a third segment "+ N more" replaces the
remaining references, e.g. "3 Nephi 5:5, Enos 1:14, + 3 more" for a word
that occurs 5 times.
"""

import csv
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CURATED_CSV_PATH = REPO_ROOT / "output" / "curated_bom_words.csv"
OCCURANCES_PATH = REPO_ROOT / "output" / "unique_bom_words_with_occurances.txt"
REFERENCES_PATH = REPO_ROOT / "output" / "unique_bom_words_references.tsv"
CATEGORIES_DIR = REPO_ROOT / "output" / "categories"

REFS_SHOWN = 2


def load_occurances() -> dict[str, int]:
    counts = {}
    with OCCURANCES_PATH.open(encoding="utf-8") as f:
        for line in f:
            word, count = line.rstrip("\n").split("\t")
            counts[word] = int(count)
    return counts


def load_references() -> dict[str, list[str]]:
    references: dict[str, list[str]] = defaultdict(list)
    with REFERENCES_PATH.open(encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            word, reference = line.rstrip("\n").split("\t")
            references[word].append(reference)
    return references


def load_curated_words() -> list[tuple[str, str]]:
    with CURATED_CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [(row["word"], row["category"]) for row in reader if row["word"]]


def format_refs(refs: list[str]) -> str:
    shown = refs[:REFS_SHOWN]
    remaining = len(refs) - len(shown)
    if remaining > 0:
        shown = shown + [f"+ {remaining} more"]
    return ", ".join(shown)


def main() -> None:
    counts = load_occurances()
    references = load_references()
    curated_words = load_curated_words()

    words_by_category: dict[str, list[str]] = defaultdict(list)
    for word, category in curated_words:
        words_by_category[category].append(word)

    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    for category, words in words_by_category.items():
        lines = [f"# {category}", ""]
        for word in words:
            refs_str = format_refs(references[word])
            lines.append(f"- {word} ({counts[word]}) - {refs_str}")
        lines.append("")
        (CATEGORIES_DIR / f"{category}.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"{category}: {len(words)} words")


if __name__ == "__main__":
    main()
