Permutation Poetry
==================

Permutation Poetry is a small Python program that uses the vast NLTK library to
generate original poetry from permutations of classic prose. It reads classic
texts like Jane Austen's "Emma" and Milton's "Paradise Lost" and finds sentences
with rhyming endings and approximately the same number of syllables. It then
picks pairs of such sentences and outputs a set of couplets that sometimes
make sense.

Examples
--------

A single couplet with 6 syllables per line and a rhyming depth of 3 phonemes on
the last word:

    It was as follows
    Aye, we men are sad fellows.

With approximately 10 syllables per line:

    We are growing a little too nice,
    I WILL be more collected--more concise.
    He is black at heart, hollow and black!
    It had been begun several days back.

Another example:

    Her observation had been pretty correct,
    my line of conduct will be more direct.
    Every invitation was successful,
    you have been here only to be useful.

And now 12 syllables per line -- so close to making sense!

    A widow Mrs Smith lodging in Westgate Buildings!
    Your dear mother was so clever at all those things!
    We have seen nothing of him since November,
    we want only two more to be just the right number.

And now getting ambitious with 16 syllables per line:

    You are speaking of letters of business; mine are letters of friendship,
    you are always labouring and toiling, exposed to every risk and hardship.

Installation
------------
Permutation poetry requires Python and the NLTK library with some additional
corpora installed. On a modern Linux system, this is quite easy. With pip
installed, running the following command installs NLTK:

    pip install nltk

Then, start the python shell and execute the following commands to install
the CMU Pronunciation Dictionary and the Project Gutenberg corpus.

    import nltk
    nltk.download()

That should pop up the NLTK Downloader window. Click on the "Corpora" section,
select "cmudict" and "gutenberg" and click "Download". That should be all.

To test if everything works, see which texts are available to NLTK by running
the following commands in the Python shell:

    from nltk.corpus import gutenberg
    gutenberg.fileids()

Usage
-----
```
    ./poet.py [number of couplets] [number of syllables per line] [rhyming threshold]

       number of couplets:  Number of sentence pairs to generate
       syllables per line:  Syllable length of extracted sentences
       rhyming threshold:   Constrain sentence pairs by # of shared trailing phonemes
```
    Defaults:

       * number of couplets: 5
       * syllables per line: 10
       * rhyming threshold:  2

Demo
----

[Paired with Flickr image search and Google web fonts](http://mayanklahiri.github.io/permutation-poetry)
