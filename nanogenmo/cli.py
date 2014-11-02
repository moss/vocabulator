from nanogenmo.documents import Document


def meatify(text):
    d = Document(text)
    for chunk in d.chunks:
        if chunk.is_noun():
            chunk.replace_with('meat')
    return str(d)
