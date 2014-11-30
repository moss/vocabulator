from itertools import cycle, filterfalse
from vocabulator.documents import PartOfSpeech


class Vocabulator:
    def __init__(self, document=None, nouns=None, adverbs=None):
        self.document = document
        self.noun_replacements = Replacements(nouns)
        if adverbs is not None:
            self.adverb_replacements = Replacements(adverbs)
        else:
            self.adverb_replacements = None

    def vocabulate(self):
        for chunk in self.document.chunks:
            if chunk.is_pos(PartOfSpeech.noun):
                replacement = self.noun_replacements.find_replacement(chunk.singular_form())
                chunk.replace_with(replacement)
            if chunk.is_pos(PartOfSpeech.adverb) and self.adverb_replacements is not None:
                replacement = self.adverb_replacements.find_replacement(chunk.word)
                chunk.replace_with(replacement)
        return str(self.document)


class Replacements:
    def __init__(self, words):
        self.seen = set()
        has_been_seen = lambda w: w in self.seen
        self.words = iter(cycle(filterfalse(has_been_seen, words)))
        self.replacements = {}

    def find_replacement(self, word):
        if word not in self.replacements:
            self.replacements[word] = self.next_replacement()
        return self.replacements[word]

    def next_replacement(self):
        replacement = next(self.words)
        self.seen.add(replacement)
        return replacement

    def print_mapping(self):
        print("\n\nReplacements Used:")
        for word in sorted(self.replacements.keys()):
            one = word
            other = self.replacements[word][0:]  # [0:] works around weirdness with Word class
            print("%s -> %s" % (one, other))


def words_from(document, pos):
    return [c.singular_form() for c in document.chunks if c.is_pos(pos)]
