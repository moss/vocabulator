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
