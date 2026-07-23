# Unique BoM Words

Finds words that appear in the 1830 first edition of the Book of Mormon but do not appear
as headwords in Webster's 1828 dictionary — the dictionary of the era in which the Book of
Mormon was published.

## Data sources

- **Dictionary**: [`websters_1828_words.txt`](data/websters_1828_words.txt) is copied verbatim
  from [`jonnyjackson26/1828-websters-dictionary`](https://github.com/jonnyjackson26/1828-websters-dictionary)
  (`words.txt`) — 62,974 headwords, one per line.
- **Book of Mormon text**: [`data/bom_1830/`](data/bom_1830) is copied from
  [`jonnyjackson26/bom-editions`](https://github.com/jonnyjackson26/bom-editions)
  (`public/data/en/1830`), one JSON file per chapter (`{"book", "chapter", "edition", "verses": [{"verse", "text"}]}`).
  That project sources its 1830 text from the
  [BYU Open Scripture Project](https://github.com/BYU-ODH/OpenScripture) and preserves original
  spelling and punctuation. It contains 6,604 verses across all 15 books, matching the known
  total verse count of the Book of Mormon.

## How it works

[`scripts/generate_unique_words.py`](scripts/generate_unique_words.py):

1. Loads the dictionary headwords into a lowercase set.
2. Walks every chapter JSON file under `data/bom_1830/`, tokenizing each verse's text into
   words (letters and internal apostrophes, e.g. `isn't`), lowercased, and counts occurrences.
3. Writes every Book of Mormon word whose lowercase form is not in the dictionary set, sorted
   alphabetically, to [`output/unique_bom_words.txt`](output/unique_bom_words.txt) as
   `word<TAB>occurrence_count`.

Proper nouns (e.g. `nephi`, `zarahemla`, `moroni`) are intentionally included — they're a
notable part of what's "unique" to the text.

Run it with:

```bash
python3 scripts/generate_unique_words.py
```

## Known limitation

Webster's 1828 lists only base/singular headwords (`Day`, `Thing`, `Word`), not inflected
forms. Common plurals and archaic verb conjugations (`days`, `things`, `hath`) therefore show
up as "unique" even though their root word is in the dictionary. No stemming/lemmatization is
applied, so the output is a literal surface-form diff, not a diff of root vocabulary.
