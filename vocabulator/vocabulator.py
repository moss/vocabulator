from itertools import cycle

__author__ = 'moss'


class Vocabulator:
    def __init__(self, document=None, nouns=None):
        self.document = document
        self.nouns = nouns

    def vocabulate(self):
        nouns = iter(cycle(self.nouns))
        for chunk in self.document.chunks:
            if chunk.is_noun():
                chunk.replace_with(next(nouns))
        return str(self.document)


def nouns_from(document):
    return [c.singular_form() for c in document.chunks if c.is_noun()]
