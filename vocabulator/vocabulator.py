from itertools import cycle, filterfalse
from textblob import Word
from vocabulator.documents import PartOfSpeech


def little_word(word):
    return len(word) < 3


def skippable_adverb(word):
    # non -ly adverbs generally prove to be bad for replacing
    return (not word.endswith('ly')) or word in {'only', 'nearly', 'previously', 'usually', 'fairly'}


def probably_not_a_name(word):
    # We're only interested in names of characters, not in all proper nouns.
    # Also, lots of words get misclassified as proper nouns, to a degree that's really ridiculous.
    # To limit this, skip all words that have dictionary definitions (except ones that are clearly people).
    return len(word) <= 3 or non_person_word(word) or word in {
        'myself',
        'his',
        'towards',
        'patagonian',
        'thine',
        'methinks',
        'civitas',
        'whaleman',
        'whilst',
    }


def non_person_word(word):
    synsets = Word(word).synsets
    if not synsets:
        return False
    non_person_meanings = [s for s in synsets if not kind_of_person(s)]
    return len(non_person_meanings) > 0


def kind_of_person(synset):
    if len(synset.hypernyms()) > 0:
        # if it has hypernyms, rather than instance hypernyms, it's probably too generic a word
        return False
    hypernym_chain = synset.closure(lambda s: s.hypernyms() + s.instance_hypernyms())
    hypernym_names = [h.name() for h in hypernym_chain]
    return 'person.n.01' in hypernym_names


class Vocabulator:
    def __init__(self, document=None, nouns=None, adverbs=None, names=None):
        self.document = document
        self.replacements_by_pos = {}
        if nouns is not None:
            self.replacements_by_pos[PartOfSpeech.noun] = Replacements(nouns, little_word)
        if adverbs is not None:
            self.replacements_by_pos[PartOfSpeech.adverb] = Replacements(adverbs, skippable_adverb)
        if names is not None:
            self.replacements_by_pos[PartOfSpeech.proper_noun] = Replacements(names, probably_not_a_name)

    def vocabulate(self):
        for chunk in self.document.chunks:
            for pos, replacements in self.replacements_by_pos.items():
                if chunk.is_pos(pos):
                    replacement = replacements.find_replacement(chunk.base_form())
                    chunk.replace_with(replacement)
        return str(self.document)


class Replacements:
    def __init__(self, words, stopword_function=little_word):
        self.seen = set()
        has_been_seen = lambda w: w in self.seen
        lower = lambda w: w.lower()
        self.words = iter(cycle(
            filterfalse(has_been_seen,
                        filterfalse(stopword_function, map(lower, words)))))
        self.stopword = stopword_function
        self.replacements = {}

    def find_replacement(self, word):
        word = word.lower()
        if self.stopword(word):
            return word
        if word not in self.replacements:
            self.replacements[word] = self.next_replacement()
        return self.replacements[word]

    def next_replacement(self):
        replacement = next(self.words)
        self.seen.add(replacement)
        return replacement

    def print_mapping(self):
        print("\n\nReplacements Used:")
        for word in sorted(self.replacements.keys()):
            one = word
            other = self.replacements[word][0:]  # [0:] works around weirdness with Word class
            print("%s -> %s" % (one, other))


def words_from(document, pos):
    return [c.base_form() for c in document.chunks if c.is_pos(pos)]
