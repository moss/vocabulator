"""
vocabulator - Create hybrid novels.

Usage:
  vocabulator (--nouns-from <noun-text> | --nouns <nouns>) <target-text>
"""
from itertools import cycle
from docopt import docopt
from vocabulator.documents import Document


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


class VocabulatorOptions:
    def __init__(self, argv=None):
        self.options = docopt(__doc__, argv=argv)

    def document(self):
        return Document.from_file(self.options['<target-text>'])

    def nouns(self):
        if self.options['--nouns-from']:
            return nouns_from(Document.from_file(self.options['<noun-text>']))
        elif self.options['--nouns']:
            return self.options['<nouns>'].split(',')

    def vocabulator(self):
        return Vocabulator(document=self.document(), nouns=self.nouns())


def vocabulator():
    opt = VocabulatorOptions()
    v = opt.vocabulator()
    print(v.vocabulate())
