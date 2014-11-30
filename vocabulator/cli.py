"""
vocabulator - Create hybrid novels.

Usage:
  vocabulator (-n <noun-text> | -N <nouns>) [-a <adverb-text>] [-m] <target-text>

Options:
  -a --adverbs-from     Specify source text for adverbs for hybrid.
  -n --nouns-from       Specify source text for nouns for hybrid.
  -N --nouns            Give a (comma-delimited) list of nouns to use.
  -m --print-mapping    List word mapping used at the end of the text.
"""
from docopt import docopt

from vocabulator.documents import Document, PartOfSpeech
from vocabulator.vocabulator import Vocabulator, words_from


class VocabulatorOptions:
    def __init__(self, argv=None):
        self.options = docopt(__doc__, argv=argv)

    def document(self):
        return Document.from_file(self.options['<target-text>'])

    def nouns(self):
        if self.options['--nouns-from']:
            return words_from(Document.from_file(self.options['<noun-text>']), PartOfSpeech.noun)
        elif self.options['--nouns']:
            return self.options['<nouns>'].split(',')

    def adverbs(self):
        if self.options['--adverbs-from']:
            return words_from(Document.from_file(self.options['<adverb-text>']), PartOfSpeech.adverb)
        else:
            return None

    def vocabulator(self):
        return Vocabulator(document=self.document(), nouns=self.nouns(), adverbs=self.adverbs())

    @property
    def print_mapping(self):
        return self.options['--print-mapping']


def vocabulator():
    opt = VocabulatorOptions()
    v = opt.vocabulator()
    print(v.vocabulate())
    print()
    if opt.print_mapping:
        print("Noun Mapping:")
        v.noun_replacements.print_mapping()
        print()
        if v.adverb_replacements:
            print("Adverb Mapping:")
            v.adverb_replacements.print_mapping()
