"""
vocabulator - Create hybrid novels.

Usage:
  vocabulator (-n <noun-text> | -N <nouns>) [-m] <target-text>

Options:
  -n --nouns-from     Specify a source text to provide nouns for the hybrid.
  -N --nouns          Give a (comma-delimited) list of nouns to use.
  -m --print-mapping  List word mapping used at the end of the text.
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

    @property
    def print_mapping(self):
        return self.options['--print-mapping']


def vocabulator():
    opt = VocabulatorOptions()
    v = opt.vocabulator()
    print(v.vocabulate())
    print()
    if opt.print_mapping:
        v.replacements.print_mapping()
