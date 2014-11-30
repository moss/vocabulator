#!/bin/bash
set -ex
export LANG=en_US.UTF-8
if [ $VIRTUALENV ]; then
    source $VIRTUALENV/bin/activate
fi
python --version
vocabulator --nouns-from pg5200.txt --adverbs-from pg2701.txt --proper-nouns-from pg2701.txt pg1342.txt > a-dream-of-large-vermin.txt
scp a-dream-of-large-vermin.txt $TARGET
