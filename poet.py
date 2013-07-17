#!/usr/bin/env python
"""
 Permutation Poetry
 Copyright 2013 Mayank Lahiri
 Released under the terms of the MIT License.
 mlahiri@gmail.com

 PERMUTATION POETRY
 ==================

 Requires:
 (1) NLTK library 
     (install via "pip install nltk")
 (2) Gutenberg and CMUDict NLTK corpora 
     (install via "import nltk" and then "nltk.download()" in Python shell)

 Usage:
   poet.py [number of couplets] [approximate syllables per line] [rhyming depth]
"""
import sys, re
from random import choice
from nltk.corpus import cmudict, gutenberg

DICTIONARY = cmudict.dict()
REPOSITORY = {}
TEXTS = [
            'austen-emma.txt', 
            'austen-persuasion.txt', 
            'austen-sense.txt', 
            'carroll-alice.txt', 
            # Feel free to add more texts here. For a full list of texts,
            # open the python shell, and run:
            #
            #  from nltk.corpus import gutenberg
            #  gutenberg.fileids()
        ]
USED_ENDINGS = []

def main(num_couplets, num_syllables, rhyme_depth):
  for text in TEXTS:
    for sentence in gutenberg.sents(text):
      addSentence(sentence, rhyme_depth)

  for couplet_number in range(0, num_couplets):
    # Get a randomly selected couplet
    attempts = 0
    while True:
      couplet = getCouplet(num_syllables)
      if couplet is not None: break
      # Prevent an infinite loop if parameters are off
      attempts += 1
      if attempts == 1000: return
    couplet = [ pretty(line) for line in couplet ]

    # A little hack for adjusting punctuation and capitalization
    couplet[0] = couplet[0][0].upper() + couplet[0][1:]
    if couplet[0][-1] == '.' or couplet[0][-1] == ',':
      couplet[0] = couplet[0][:-1] + ','
      char = couplet[1][0].lower() if couplet[1][:2] != 'I ' else 'I'
      couplet[1] = char + couplet[1][1:]
    else:
      couplet[1] = couplet[1][0].upper() + couplet[1][1:]

    # Dump to stdout
    print couplet[0]
    print couplet[1]

def addSentence(sentence, rhyme_depth):
  """Analyze an array of words and add it to the sentence REPOSITORY."""
  if len(sentence) > 20: return
  recognized_words = [ w.lower() for w in sentence if w.lower() in DICTIONARY ]
  if len(recognized_words) < 3: return

  # pronounced = phonetic pronunciation and syllable count from CMUDict
  pronounced = [ DICTIONARY[w][0] for w in recognized_words ]

  # CMUDict uses a weird format where a number as the last character represents
  # a syllable (not the number of syllables, just the fact that one is present)
  syllables = [ len([ y for y in x if y[-1].isdigit() ]) for x in pronounced ]
  num_syllables = sum(syllables)

  # The rhyme ending is the last n phonemes from the pronunciation of the 
  # last word. It's not perfect, but it works well enough.
  rhyme_ending = tuple(pronounced[-1][-rhyme_depth:])

  # Create a record for the sentence
  record = (recognized_words[-1], num_syllables, sentence)

  # Save this sentence keyed by the rhyme-ending
  if rhyme_ending not in REPOSITORY: REPOSITORY[rhyme_ending] = []
  REPOSITORY[rhyme_ending].append(record)

def getCouplet(num_syll):
  """Generate a couplet with an approximate number of syllables, or return None."""
  ending = choice(REPOSITORY.keys())            # random rhyme ending
  if ending in USED_ENDINGS: return None        # used already? if so, abort
  line1 = choice(REPOSITORY[ending])            # two random lines with chosen rhyme ending
  line2 = choice(REPOSITORY[ending])
  if line1[0] == line2[0]: return None          # same last word in both lines
  if abs(line1[1] - num_syll) > 1: return None  # wrong syllable count +/- 1 syllable
  if abs(line2[1] - num_syll) > 1: return None  # wrong syllable count +/- 1 syllable
  USED_ENDINGS.append(ending)                   # don't use this rhyme ending again
  return (line1[-1], line2[-1])

def pretty(words):
  """Some heuristics to adjust punctuation and spacing in a word array."""
  words = ' '.join(words)
  words = re.sub('\s*([\'\?\;\-\!])\s*', '\\1', words)  # extraneous spaces
  words = re.sub('\s*([;\.,])\s*', '\\1 ', words)       # space before punctuation
  words = re.sub('^[\'"]|["\']$', '', words)            # beginning and ending quotes
  words = re.sub('[":`_\(\)]', '', words)               # punctuation we just don't like
  words = re.sub('\s\s*', ' ', words)                   # extraneous whitespace
  words = words.strip()                                 # leading and trailing whitespace
  return words

if __name__ == '__main__': 
  arg_num_couplets = 5
  arg_num_syllables = 10
  arg_rhyme_depth = 2
  if len(sys.argv) >= 2: arg_num_couplets = int(sys.argv[1])
  if len(sys.argv) >= 3: arg_num_syllables = int(sys.argv[2])
  if len(sys.argv) >= 4: arg_rhyme_depth = int(sys.argv[3])
  main(arg_num_couplets, arg_num_syllables, arg_rhyme_depth)
