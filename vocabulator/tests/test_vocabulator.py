from vocabulator.documents import Document
from vocabulator.vocabulator import Vocabulator, nouns_from, Replacements

SOURCE_TEXT = """
Once there was a man.  He had a hat.  He went to a party.  He was very
bored!  When the party was over he went home and ate cake.  It was
delicious!  The cake was so filling that he went to sleep.

When he woke up, he had to go buy some tools.  It was boring too.
"""

ANOTHER_SOURCE = """
Winston was a scientist. One day he ventured into the woods. He found
a badger with purple spines!
"""


def test_meatify():
    v = Vocabulator(document=Document(SOURCE_TEXT), nouns=['meat'])
    assert v.vocabulate() == """
Once there was a meat.  He had a meat.  He went to a meat.  He was very
bored!  When the meat was over he went meat and ate meat.  It was
delicious!  The meat was so filling that he went to sleep.

When he woke up, he had to go buy some meat.  It was boring too.
"""


def test_swap_nouns():
    v = Vocabulator(document=Document(SOURCE_TEXT), nouns=nouns_from(Document(ANOTHER_SOURCE)))
    assert v.vocabulate() == """
Once there was a scientist.  He had a day.  He went to a wood.  He was very
bored!  When the wood was over he went badger and ate spine.  It was
delicious!  The spine was so filling that he went to sleep.

When he woke up, he had to go buy some scientists.  It was boring too.
"""


def test_swap_nouns_the_other_way():
    v = Vocabulator(document=Document(ANOTHER_SOURCE), nouns=nouns_from(Document(SOURCE_TEXT)))
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
