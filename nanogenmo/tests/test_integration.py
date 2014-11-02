from nanogenmo.cli import meatify

SOURCE_TEXT = """
Once there was a man.  He had a hat.  He went to a party.  He was very
bored!  When the party was over he went home and ate cake.  It was
delicious!  The cake was so filling that he went to sleep.

When he woke up, he had to go buy some tools.  It was boring too.
"""

AFTER_MEATIFYING = """
Once there was a meat.  He had a meat.  He went to a meat.  He was very
bored!  When the meat was over he went meat and ate meat.  It was
delicious!  The meat was so filling that he went to sleep.

When he woke up, he had to go buy some meats.  It was boring too.
"""


def test_integration():
    assert meatify(SOURCE_TEXT) == AFTER_MEATIFYING
