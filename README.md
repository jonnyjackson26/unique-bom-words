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

## What counts as a "word"

`scripts/generate_unique_words.py` scans each verse's `text` with the regular expression
`[A-Za-z'’-]+` — a maximal run of Latin letters that may also contain straight (`'`) or curly
(`’`) apostrophes, or hyphens (`-`) — then, from each match:

1. **Removes every apostrophe** (straight or curly), rather than treating it as part of the
   word or as a word boundary. `Lord’s` and `Lord's` both become `lords`; `father's` becomes
   `fathers`. (The 1830 text in this repo only ever uses the curly `’`, e.g. `Lord’s`,
   `shoe’s`, `cockatrice’s` — the straight-apostrophe case is handled for robustness but
   doesn't currently occur.)
2. **Keeps hyphens as-is** — a hyphen does *not* split the word. `to-day` stays `to-day`;
   `Ani-anti` (Alma 21:11) stays `ani-anti`; `Anti-Nephi-Lehi`, `Lehi-Nephi` (the city), and
   `Maher-shalal-hash-baz` each stay a single hyphenated word.
3. **Lowercases** the result, e.g. `Nephi` and `nephi` are the same word.

Everything else — spaces, commas, periods, semicolons, colons, question marks, exclamation
points, em dashes (`—`), parentheses, and square brackets — is treated as a word boundary, not
part of a word. Bracketed editorial insertions are counted as ordinary text, e.g. `[hoofs]` in
3 Nephi 20:19 contributes the word `hoofs`.

Each resulting word is then counted per occurrence (across all 6,604 verses) and, if its
lowercase form isn't a headword in Webster's 1828, written to the output files:

- [`output/unique_bom_words.txt`](output/unique_bom_words.txt) — one word per line, sorted
  alphabetically, no occurrence counts.
- [`output/unique_bom_words_with_occurances.txt`](output/unique_bom_words_with_occurances.txt) —
  `word<TAB>occurrence_count`, same words and order, with counts.
- [`output/unique_bom_words_references.tsv`](output/unique_bom_words_references.tsv) —
  `word<TAB>reference`, one row per occurrence (e.g. `zarahemla	Omni 1:13`), so every
  occurrence of every unique word can be traced back to its verse.

Proper nouns (e.g. `nephi`, `zarahemla`, `moroni`) are intentionally included — they're a
notable part of what's "unique" to the text.

Run it with:

```bash
python3 scripts/generate_unique_words.py
```

## Curated categories

[`output/curated_bom_words.csv`](output/curated_bom_words.csv) is a hand-reviewed, manually
curated CSV (`word,category,notes`) classifying every word in `unique_bom_words.txt` into a
category (`Proper`, `Typo`, `Variation`, `Real`, as of this writing).

[`scripts/generate_category_pages.py`](scripts/generate_category_pages.py) reads that CSV and
writes one Markdown file per category to `output/categories/<category>.md`, e.g.
[`output/categories/Proper.md`](output/categories/Proper.md). Each is a bullet list, one line
per word:

```
- abinadi (37) - [Mosiah 11:20](https://bom-editions.vercel.app/en/1830/mosiah/11#20), [Mosiah 11:26](https://bom-editions.vercel.app/en/1830/mosiah/11#26), + 35 more
- abish (1) - [Alma 19:16](https://bom-editions.vercel.app/en/1830/alma/19#16)
```

`(N)` is the word's total occurrence count; after it, up to the first 2 verse references are
shown as links to that verse's page on the [Book of Mormon Editions
Project](https://bom-editions.vercel.app)'s 1830 edition (e.g. `Mosiah 11:20` →
`https://bom-editions.vercel.app/en/1830/mosiah/11#20`), and if the word occurs more than
twice, a final `+ N more` segment (not linked) covers the rest.

Run it with:

```bash
python3 scripts/generate_category_pages.py
```

## Known limitation

Webster's 1828 lists only base/singular headwords (`Day`, `Thing`, `Word`), not inflected
forms. Common plurals and archaic verb conjugations (`days`, `things`, `hath`) therefore show
up as "unique" even though their root word is in the dictionary. No stemming/lemmatization is
applied, so the output is a literal surface-form diff, not a diff of root vocabulary.
