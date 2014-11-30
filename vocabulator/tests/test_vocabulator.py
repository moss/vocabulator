from vocabulator.documents import Document, PartOfSpeech
from vocabulator.vocabulator import Vocabulator, words_from, Replacements, little_word

SOURCE_TEXT = """
Once there was a man.  He had a hat.  He went to a party.  He was very
bored!  When the party was over he went home and ate cake.  It was
delicious!  The cake was so filling that he went immediately to sleep.

When he woke up, he had to go buy some tools.  It was boring too.
"""

ANOTHER_SOURCE = """
Winston was a scientist. One day he ventured into the woods. He found
a badger with purple spines!
"""


def test_meatify():
    v = Vocabulator(document=Document(SOURCE_TEXT), nouns=['meat'], adverbs=['dreamily'])
    assert v.vocabulate() == """
Once there was a meat.  He had a meat.  He went to a meat.  He was very
bored!  When the meat was over he went meat and ate meat.  It was
delicious!  The meat was so filling that he went dreamily to sleep.

When he woke up, he had to go buy some meat.  It was boring too.
"""


def Xtest_proper_nouns():
    v = Vocabulator(document=Document("Bob went to the store."), proper_nouns=['Jill'])
    assert v.vocabulate() == "Jill went to the store."


def test_swap_nouns():
    v = Vocabulator(document=Document(SOURCE_TEXT), nouns=words_from(Document(ANOTHER_SOURCE), PartOfSpeech.noun))
    assert v.vocabulate() == """
Once there was a scientist.  He had a day.  He went to a wood.  He was very
bored!  When the wood was over he went badger and ate spine.  It was
delicious!  The spine was so filling that he went immediately to sleep.

When he woke up, he had to go buy some scientists.  It was boring too.
"""


def test_swap_nouns_the_other_way():
    v = Vocabulator(document=Document(ANOTHER_SOURCE), nouns=words_from(Document(SOURCE_TEXT), PartOfSpeech.noun))
    assert v.vocabulate() == """
Winston was a man. One hat he ventured into the parties. He found
a home with purple cakes!
"""


def test_replacements_will_replace_stably_and_avoid_reusing_duplicated_words():
    r = Replacements(['elbow', 'hand', 'arm', 'hand', 'eye'])
    assert r.find_replacement('bowl') == 'elbow'
    assert r.find_replacement('table') == 'hand'
    assert r.find_replacement('table') == 'hand'  # stable replacements for same word
    assert r.find_replacement('chair') == 'arm'
    assert r.find_replacement('table') == 'hand'  # stable replacements for same word later on
    assert r.find_replacement('desk') == 'eye'  # skips duplicates in source noun list
    assert r.find_replacement('lens') == 'elbow'  # finally does loop back around again


def test_replacing_a_word_preserves_case():
    d = Document('This is A TEST.')
    d.chunks[0].replace_with('something')
    d.chunks[2].replace_with('was')
    d.chunks[4].replace_with('the')
    d.chunks[6].replace_with('result')
    assert str(d) == 'Something was The RESULT.'


def test_replacements_are_printable(capsys):
    r = Replacements(['Elbow', 'hand', 'ARM', 'Hand', 'eye'])
    for w in ['bowl', 'Table', 'chair', 'DESK', 'lens', 'desk']:
        r.find_replacement(w)
    r.print_mapping()
    out, err = capsys.readouterr()
    assert out == """

Replacements Used:
bowl -> elbow
chair -> arm
desk -> eye
lens -> elbow
table -> hand
"""


def test_replacements_ignore_stopwords():
    r = Replacements(['elbow', 'a', 'n', 't'], little_word)
    # should not replace stopwords:
    assert r.find_replacement('n') == 'n'
    assert r.find_replacement('w') == 'w'
    assert r.find_replacement('it') == 'it'
    # should not use stopwords from replacement source:
    assert r.find_replacement('hat') == 'elbow'
    assert r.find_replacement('cat') == 'elbow'


def test_should_not_mistake_things_for_nouns_if_they_have_no_letters():
    d = Document('_You_ want to tell me, and I have no objection to hearing it.')
    first_chunk = d.chunks[0]
    assert first_chunk.word == '_'  # if not, this test needs updating
    assert not first_chunk.is_pos(PartOfSpeech.noun)
