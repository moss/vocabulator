from itertools import cycle, filterfalse

__author__ = 'moss'


class Vocabulator:
    def __init__(self, document=None, nouns=None):
        self.document = document
        self.nouns = nouns

    def vocabulate(self):
        replacements = Replacements(self.nouns)
        for chunk in self.document.chunks:
            if chunk.is_noun():
                replacement = replacements.find_replacement(chunk.singular_form())
                chunk.replace_with(replacement)
        return str(self.document)


class Replacements:
    def __init__(self, nouns):
        self.seen = set()
        has_been_seen = lambda w: w in self.seen
        self.nouns = iter(cycle(filterfalse(has_been_seen, nouns)))
        self.replacements = {}

    def find_replacement(self, word):
        if word not in self.replacements:
            self.replacements[word] = self.next_replacement()
        return self.replacements[word]

    def next_replacement(self):
        replacement = next(self.nouns)
        self.seen.add(replacement)
        return replacement


def nouns_from(document):
    return [c.singular_form() for c in document.chunks if c.is_noun()]
