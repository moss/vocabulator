from itertools import cycle
from docopt import docopt
from vocabulator.documents import Document


class Vocabulator:
    def __init__(self):
        self.document = None
        self.nouns = None

    def use_document(self, document_file):
        self.document = Document.from_file(document_file)

    def use_document_text(self, document_text):
        self.document = Document(document_text)

    def use_nouns(self, nouns):
        self.nouns = nouns

    def use_nouns_from(self, noun_text_file):
        noun_document = Document.from_file(noun_text_file)
        self.nouns = self.nouns_from(noun_document)

    def use_nouns_from_text(self, noun_text):
        noun_document = Document(noun_text)
        self.nouns = self.nouns_from(noun_document)

    def vocabulate(self):
        nouns = iter(cycle(self.nouns))
        for chunk in self.document.chunks:
            if chunk.is_noun():
                chunk.replace_with(next(nouns))
        return str(self.document)

    @staticmethod
    def nouns_from(document):
        return [c.singular_form() for c in document.chunks if c.is_noun()]


def vocabulator():
    """
    Create hybrid novels.

    Usage:
      vocabulator (--nouns-from <noun-text> | --nouns <nouns>) <target-text>
    """
    opt = docopt(vocabulator.__doc__)
    v = Vocabulator()
    v.use_document(opt['<target-text>'])
    if opt['--nouns-from']:
        v.use_nouns_from(opt['<noun-text>'])
    elif opt['--nouns']:
        v.use_nouns(opt['<nouns>'].split(','))
    print(v.vocabulate())
