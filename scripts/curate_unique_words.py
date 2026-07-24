#!/usr/bin/env python3
"""Manually-curated categorization of the unique BoM words into output/curated.md.

This is a hand-reviewed classification (encoded as explicit word lists below,
compiled by reading through every entry in output/unique_bom_words.txt), not a
purely automated heuristic. Suffix rules are only used to bucket the large,
unambiguous set of plain plurals/verb-tense forms; every word that doesn't
clearly match one of the other categories falls back to Names & Places, since
the Book of Mormon's unique vocabulary is dominated by invented proper nouns.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORDS_PATH = REPO_ROOT / "output" / "unique_bom_words.txt"
DICTIONARY_PATH = REPO_ROOT / "data" / "websters_1828_words.txt"
OUTPUT_PATH = REPO_ROOT / "output" / "curated.md"

# Words that are typos, OCR/print artifacts, or archaic/period spelling variants
# of ordinary English words.
TYPOS_AND_VARIANTS = {
    "aaswer", "abridgement", "adhear", "adminster", "ancles", "armour",
    "armours", "armss", "arrriven", "asmuch", "atempt", "axe", "bablings",
    "babtized", "bacause", "baptise", "baptised", "becaus", "betweem",
    "befal", "brethern", "carcases", "centre", "changeble", "cimeter",
    "cimeters", "citties", "clowd", "commmandments", "condescention",
    "condescentions", "continnally", "counselled", "counsellor", "daghter",
    "darknesss", "deadnes", "defence", "dependant", "devlish", "dissention",
    "dissentions", "drunkennes", "eigth", "engravened", "evidencess",
    "excedingly", "feading", "firy", "fraid", "fulfil", "fulness",
    "govereor", "harrass", "havgn", "heen", "hehold", "immoveable",
    "journied", "judgement", "judgements", "khown", "laboured", "langauge",
    "levelled", "lustre", "marvelled", "marvelling", "marvellings",
    "marvellous", "mnltitude", "mouldering", "moulten", "neckedness",
    "neeeds", "neverthelers", "nevertheles", "numhers", "obout", "offence",
    "opon", "peeple", "peopeople", "plaees", "possesion", "possessson",
    "prohesy", "prophecying", "prophecyings", "provisons", "quarrellings",
    "realise", "reccive", "recieve", "recieved", "recieveth", "recieving",
    "redemer", "regin", "rehearst", "rerecord", "rssurrection", "rufused",
    "rumderers", "savour", "saviour", "sceptres", "seeond", "sepulchre",
    "skilful", "suredly", "swolen", "tempels", "theit", "therefere",
    "therfore", "thess",
    "transgransgressions", "travelled", "traveller", "travelling",
    "treusures", "threatnings", "uncircumsised", "understandding", "vails",
    "vapour", "wat", "wherfore", "whieh", "wildernsss", "wilfully",
    "wilfulness", "worshippers", "wrent", "writen",
}

# Archaic verb conjugations and archaic diction ("thou hearest", "he hath",
# "it came to pass, insomuch that"), distinct from ordinary modern inflections.
OLD_ENGLISH = {
    # irregular archaic forms
    "hath", "doth", "saith",
    # archaic 2nd-person ("thou ...") verb conjugations and modal contractions
    "abhorrest", "beheldest", "beholdest", "believest", "canst", "commandest",
    "comfortedst", "considerest", "deniest", "desirest", "didst", "doest",
    "dwellest", "forgetest", "hadst", "heardest", "hearest", "knewest",
    "knowest", "livest", "lovest", "madest", "mayest", "mightest",
    "rememberest", "risest", "saidst", "sawest", "sayest", "shouldest",
    "shouldst", "wouldest", "wouldst",
    # archaic strong-verb past/participle forms
    "arriven", "begat", "chid", "graven",
    # archaic KJV-style spelling of show/showed/shown
    "shew", "shewed", "shewn",
    # archaic diction and conjunctions
    "beforetime", "burthens", "burthensome", "forasmuch", "inasmuch",
    "rereward", "selfsame", "withersoever",
}

# Real English words that are simply absent from the 1828 word list as a
# distinct headword, but aren't typos, archaic forms, plurals/verb-tenses, or
# proper nouns -- odd compounds, rare abstract nouns, or ambiguous fragments.
OTHER = {
    "ahah", "bestow", "breastwork", "candlestick", "carbuncles",
    "circumcision", "byword", "entrusted", "eyewitness", "faggots",
    "farthermost", "firstly", "forever", "havoc", "headplates",
    "hinderment", "information", "ites", "maidservants", "miserable",
    "northernmost", "numerority", "overbearance", "pestilence",
    "pestilences", "preparator", "revelator", "silverlings", "stiffnecked",
    "stiffneckedness", "storehouse", "subtlety", "traffic",
    "unwearyingness", "upside", "vexation", "woundedness",
}

# Irregular inflections whose base word is in the dictionary but isn't caught
# by the simple suffix-stripping rules below (vowel changes, consonant
# doubling, irregular plurals, etc.).
FORCE_INFLECTIONS = {
    "began", "bidden", "digging", "dimmed", "drew", "dwelt", "easier",
    "forbade", "forbidden", "foretold", "freemen", "glutting", "happier",
    "hemmed", "knelt", "known", "letting", "marred", "mightier",
    "overcame", "overran", "overtaken", "overthrew", "oxen", "permitted",
    "retaken", "shaven", "sinned", "sixteenth", "slipped", "spent",
    "watchmen", "withdrew", "withstood", "wolves", "workmen", "yourselves",
}

# Proper nouns that could be mistaken for something else by the suffix rules
# below (e.g. gentilic plurals like "nephites"), forced into Names & Places.
FORCE_NAMES_AND_PLACES = {
    "deseret",  # Jaredite word for "honeybee" (Ether 2:3), treated as a proper term
}

WORDS_ENDS = ("ies", "es", "s", "ied", "ed", "ing", "est", "er")


def load_word_set(path: Path) -> set[str]:
    with path.open(encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def load_word_counts(path: Path) -> dict[str, int]:
    counts = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            word, count = line.rstrip("\n").split("\t")
            counts[word] = int(count)
    return counts


def inflection_base_candidates(word: str) -> list[str]:
    candidates = []
    if word.endswith("ies") and len(word) > 4:
        candidates.append(word[:-3] + "y")
    if word.endswith("ied") and len(word) > 4:
        candidates.append(word[:-3] + "y")
    if word.endswith("es"):
        candidates.append(word[:-2])
        candidates.append(word[:-1])
    if word.endswith("s") and not word.endswith("ss"):
        candidates.append(word[:-1])
    if word.endswith("ed"):
        candidates.append(word[:-2])
        candidates.append(word[:-1])
    if word.endswith("ing"):
        candidates.append(word[:-3])
        candidates.append(word[:-3] + "e")
    if word.endswith("est"):
        candidates.append(word[:-3])
        candidates.append(word[:-2])
    if word.endswith("er"):
        candidates.append(word[:-2])
        candidates.append(word[:-1])
    return candidates


def classify(word: str, dictionary_words: set[str]) -> str:
    if word in TYPOS_AND_VARIANTS:
        return "typos"
    if word in OLD_ENGLISH:
        return "old_english"
    if word in OTHER:
        return "other"
    if word in FORCE_INFLECTIONS:
        return "inflections"
    if word in FORCE_NAMES_AND_PLACES:
        return "names_and_places"
    if word.endswith("eth") and len(word) > 4:
        return "old_english"
    for base in inflection_base_candidates(word):
        if base in dictionary_words:
            return "inflections"
    return "names_and_places"


SECTIONS = [
    ("inflections", "Plurals & Inflections",
     "Ordinary plural, tense, or comparative forms of words that already exist "
     "in Webster's 1828 as a base headword (e.g. `Ancient` -> `ancients`, "
     "`Begin` -> `began`). These are the largest category, and mostly an "
     "artifact of the dictionary listing only base/singular headwords."),
    ("old_english", "Old English / Archaic Forms",
     "Archaic verb conjugations (`hath`, `doth`, `saith`, `-eth`/`-est` "
     "endings for \"he\"/\"thou\") and archaic diction, distinct from modern "
     "inflections above."),
    ("names_and_places", "Names & Places",
     "Proper nouns: people, peoples/gentilics, and places invented in or "
     "carried over into the Book of Mormon."),
    ("typos", "Typos & Spelling Variants",
     "Apparent print/transcription errors in the 1830 first edition, plus "
     "period British/archaic spelling variants of ordinary words (e.g. "
     "`armour`, `judgement`)."),
    ("other", "Other",
     "Real English words that don't fit the categories above -- rare "
     "compounds or abstract nouns simply missing from the 1828 headword "
     "list, and ambiguous fragments."),
]


def main() -> None:
    dictionary_words = load_word_set(DICTIONARY_PATH)
    word_counts = load_word_counts(WORDS_PATH)

    buckets: dict[str, list[str]] = {key: [] for key, _, _ in SECTIONS}
    for word in sorted(word_counts):
        buckets[classify(word, dictionary_words)].append(word)

    lines = [
        "# Curated Unique BoM Words",
        "",
        "A manually-reviewed breakdown of `output/unique_bom_words.txt` "
        "(words in the 1830 Book of Mormon not found in Webster's 1828 "
        "dictionary), grouped by why each word is \"unique.\" Generated by "
        "`scripts/curate_unique_words.py`, which encodes the category "
        "assignments reviewed by hand.",
        "",
    ]
    for key, title, blurb in SECTIONS:
        words = buckets[key]
        lines.append(f"## {title} ({len(words)})")
        lines.append("")
        lines.append(blurb)
        lines.append("")
        for word in words:
            lines.append(f"- {word} ({word_counts[word]})")
        lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    for key, title, _ in SECTIONS:
        print(f"{title}: {len(buckets[key])}")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
