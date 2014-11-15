from itertools import cycle, filterfalse


class Vocabulator:
    def __init__(self, document=None, nouns=None):
        self.document = document
        self.replacements = Replacements(nouns)
        self.nouns = nouns

    def vocabulate(self):
        for chunk in self.document.chunks:
            if chunk.is_noun():
                replacement = self.replacements.find_replacement(chunk.singular_form())
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

    def print_mapping(self):
        print("\n\nReplacements Used:")
        for word in sorted(self.replacements.keys()):
            one = word
            other = self.replacements[word][0:]  # [0:] works around weirdness with Word class
            print("%s -> %s" % (one, other))


def nouns_from(document):
    return [c.singular_form() for c in document.chunks if c.is_noun()]
