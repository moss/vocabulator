"""
vocabulator - Create hybrid novels.

Usage:
  vocabulator (--nouns-from <noun-text> | --nouns <nouns>) <target-text>
"""
from docopt import docopt

from vocabulator.documents import Document
from vocabulator.vocabulator import Vocabulator, nouns_from


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
