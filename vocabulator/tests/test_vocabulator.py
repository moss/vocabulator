from vocabulator.cli import Vocabulator

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
    v = Vocabulator()
    v.use_document_text(SOURCE_TEXT)
    v.use_nouns(['meat'])
    assert v.vocabulate() == """
Once there was a meat.  He had a meat.  He went to a meat.  He was very
bored!  When the meat was over he went meat and ate meat.  It was
delicious!  The meat was so filling that he went to sleep.

When he woke up, he had to go buy some meat.  It was boring too.
"""


def test_swap_nouns():
    v = Vocabulator()
    v.use_document_text(SOURCE_TEXT)
    v.use_nouns_from_text(ANOTHER_SOURCE)
    assert v.vocabulate() == """
Once there was a scientist.  He had a day.  He went to a wood.  He was very
bored!  When the badger was over he went spine and ate scientist.  It was
delicious!  The day was so filling that he went to sleep.

When he woke up, he had to go buy some woods.  It was boring too.
"""

def test_swap_nouns_the_other_way():
    v = Vocabulator()
    v.use_document_text(ANOTHER_SOURCE)
    v.use_nouns_from_text(SOURCE_TEXT)
    assert v.vocabulate() == """
Winston was a man. One hat he ventured into the parties. He found
a party with purple homes!
"""
