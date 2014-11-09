from itertools import cycle
import sys
from nanogenmo.documents import Document


def meatify(text):
    d = Document(text)
    for chunk in d.chunks:
        if chunk.is_noun():
            chunk.replace_with('meat')
    return str(d)


def meatify_cmd():
    filename = sys.argv[1]
    with open(filename) as f:
        text = f.read()
        print(meatify(text))


def nouns_from(document):
    return [c.singular_form() for c in document.chunks if c.is_noun()]


def swap_nouns(target, source):
    target = Document(target)
    source = Document(source)
    nouns = iter(cycle(nouns_from(source)))
    for chunk in target.chunks:
        if chunk.is_noun():
            chunk.replace_with(next(nouns))
    return str(target)


def swap_nouns_cmd():
    with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2:
        print(swap_nouns(f1.read(), f2.read()))
