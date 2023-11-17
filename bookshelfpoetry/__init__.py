import pandas as pd
from dataclasses import dataclass
from functools import cached_property
from typing import Self, TypeAlias, NamedTuple, Iterable
from collections import defaultdict
import random


class CorpusRow(NamedTuple):
    dhlabid: str
    urn: str
    title: str
    authors: str
    oaiid: str
    sesamid: str
    isbn10: str
    city: str
    timestamp: str
    year: str
    publisher: str
    langs: str
    subjects: str
    ddc: str
    genres: str
    literaryform: str
    doctype: str
    ocr_creator: str
    ocr_timestamp: str


Corpus: TypeAlias = Iterable[CorpusRow]


def estimate_norwegian_syllables(text: str) -> int:
    """Estimate the number of syllables in a norwegian text by counting vowels.
    This is only a heuristic and will not account for e.g. diphthongs.

    Parameters
    ----------
    text: str
        Text to count syllables in. Assumed to be in Norwegian.

    Returns
    -------
    int:
        The estimated number of syllabes in the input text.
    """

    vokaler = "aeiouyæøå"
    num_syllables = 0
    for letter in text.lower():
        if letter in vokaler:
            num_syllables += 1
    return num_syllables


@dataclass(frozen=True)
class Text:
    title: str
    urn: str

    @cached_property
    def num_syllables(self) -> int:
        return estimate_norwegian_syllables(self.title)

    @cached_property
    def url(self) -> str:
        return f"https://www.nb.no/items/{self.urn}"

    @classmethod
    def from_corpus_row(cls, corpus_row: CorpusRow) -> Self:
        return cls(title=corpus_row.title, urn=corpus_row.urn)


SyllableIndex: TypeAlias = dict[int, list[Text]]
TitlePoem: TypeAlias = tuple[Text, Text, Text]


def get_syllable_counts(corpus: Corpus) -> SyllableIndex:
    """Get index of texts in corpus based on no. syllables in the title

    Parameters
    ----------
    corpus: Corpus
        Corpus to create index from

    Returns
    -------
    SyllableIndex
        An index of texts in corpus based on no. syllables in the title

    """
    syllable_counts = defaultdict(list)
    for row in corpus:
        text = Text.from_corpus_row(row)
        if text.num_syllables in [5, 7, 12, 17]:
            syllable_counts[text.num_syllables].append(text)
    return syllable_counts


def get_random_poem(syllable_counts: SyllableIndex) -> TitlePoem:
    """Creates a random haiku by picking text titles with 5, 7 and 5 syllables

    Parameters
    ----------
    syllable_counts: SyllableIndex
        Index of text based on syllables

    Returns
    -------
    TitleHaiku
        tuple containing three phrases of with five, seven and five syllables.
    """

    phrase1, phrase3 = random.sample(syllable_counts[5], 2)
    phrase2 = random.sample(syllable_counts[7], 1)[0]
    return phrase1, phrase2, phrase3


if __name__ == "__main__":
    corpus = pd.read_excel("assets/korpus.xlsx").itertuples()
    syllable_counts = get_syllable_counts(corpus)

    for haiku_num in range(3):
        haiku = get_random_poem(syllable_counts)
        print(haiku)
