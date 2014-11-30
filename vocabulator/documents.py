from enum import Enum
import re
from textblob import TextBlob, Word
from textblob.en.inflect import pluralize


class Document:
    def __init__(self, source=""):
        self.source = source
        self.blob = TextBlob(source)
        self.chunks = list(self._calculate_chunks())

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return Document(f.read())

    def _calculate_chunks(self):
        position = 0
        for word, tag in self.blob.pos_tags:
            start_position = self.source.find(word, position)
            end_position = start_position + len(word)
            if start_position > position:
                yield InterstitialChunk(source=self.source, start=position, end=start_position)
            yield DocWord(source=self.source, word=word, start=start_position, end=end_position)
            position = end_position
        if position < len(self.source):
            yield InterstitialChunk(self.source, position, len(self.source))

    def __str__(self):
        return ''.join(str(c) for c in self.chunks)


class PartOfSpeech(Enum):
    noun = ('NN', 'NNS')
    adverb = ('RB')

    def __init__(self, *options):
        self.options = options


class Chunk:
    def __init__(self, source="", start=0, end=0):
        self.source = source
        self.start = start
        self.end = end
        self.replacement = None

    def replace_with(self, replacement):
        self.replacement = self.match_original_formatting(replacement)

    @property
    def original(self):
        return self.source[self.start:self.end]

    def __str__(self):
        return self.replacement or self.original

    def match_original_formatting(self, replacement):
        if self.original.istitle():
            return replacement.title()
        if self.original.isupper():
            return replacement.upper()
        return replacement


class InterstitialChunk(Chunk):
    def is_pos(self, pos: PartOfSpeech):
        return False


class DocWord(Chunk):
    def __init__(self, source, word: Word, start=0, end=0):
        super().__init__(source, start, end)
        self.word = word
        self.replacement = None

    @property
    def pos_tag(self):
        """
        Part of speech tag, which could be one of:
          CC, CD, DT, EX, FW, IN, JJ, JJR, JJS, MD, NN, NNP, NNS, POS,
          PRP, PRP$, RB, RBR, RBS, TO, UH, VB, VBD, VBG, VBN, VBP, VBZ,
          WDT, WP, WP$, WRB
        """
        return self.word.pos_tag

    def is_pos(self, pos: PartOfSpeech):
        if not re.match(r"[A-Za-z']+$", self.word):
            return False
        return self.pos_tag in pos.options

    def singular_form(self):
        return self.word.singularize()

    def replace_with(self, replacement):
        if self.pos_tag == 'NNS':
            super().replace_with(pluralize(replacement))
        else:
            super().replace_with(replacement)
