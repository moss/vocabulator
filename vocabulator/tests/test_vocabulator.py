from vocabulator.cli import meatify, swap_nouns

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
    assert meatify(SOURCE_TEXT) == """
Once there was a meat.  He had a meat.  He went to a meat.  He was very
bored!  When the meat was over he went meat and ate meat.  It was
delicious!  The meat was so filling that he went to sleep.

When he woke up, he had to go buy some meat.  It was boring too.
"""


def test_swap_nouns():
    assert swap_nouns(SOURCE_TEXT, ANOTHER_SOURCE) == """
Once there was a scientist.  He had a day.  He went to a wood.  He was very
bored!  When the badger was over he went spine and ate scientist.  It was
delicious!  The day was so filling that he went to sleep.

When he woke up, he had to go buy some woods.  It was boring too.
"""
    assert swap_nouns(ANOTHER_SOURCE, SOURCE_TEXT) == """
Winston was a man. One hat he ventured into the parties. He found
a party with purple homes!
"""
