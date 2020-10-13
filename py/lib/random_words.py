from datetime import datetime, timedelta
import os
import pickle
import random
import re

from typing import Set

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
WORD_LIST_PICKLE = os.path.join(THIS_DIR, 'random_words.pickle')

BROWN_ADJECTIVES = 'JJ'
BROWN_PRESENT_PARTICIPLE_VERB = 'VBG'
BROWN_PAST_PARTICIPLE_VERB = 'VBN'
BROWN_PLURAL_NOUN = 'NNS'
BROWN_PROPER_PLURAL_NOUN = 'NPS'
BROWN_NOUN = 'NN'


def regenerate_word_lists():
    from nltk.corpus import brown

    tagged_words = brown.tagged_words()
    regex = re.compile(r'^[a-z][a-z0-9]*$')

    def is_dns_friendly(s: str):
        return bool(regex.match(s))

    prefix_tags = [BROWN_PRESENT_PARTICIPLE_VERB, BROWN_PAST_PARTICIPLE_VERB, BROWN_ADJECTIVES]
    prefixes = {word.lower() for (word, tag) in tagged_words if tag in prefix_tags and is_dns_friendly(word)}

    noun_tags = [BROWN_PLURAL_NOUN, BROWN_PROPER_PLURAL_NOUN, BROWN_NOUN]
    nouns = {word.lower() for (word, tag) in tagged_words if tag in noun_tags and is_dns_friendly(word)}

    with open(WORD_LIST_PICKLE, 'wb') as f:
        pickle.dump({'prefixes': prefixes, 'nouns': nouns}, f)


def get_word_lists():
    with open(WORD_LIST_PICKLE, 'rb') as f:
        data = pickle.load(f)
        return data['prefixes'], data['nouns']


ENTERTAINING_ALLITERATIVE_NGRAMS = ['bb', 'dd', 'll', 'k', 'pp', 'rr', 'ss', 'tt']
CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']


def pleasing_combination(word1, word2):
    # Contains entertaining alliterative ngrams
    for ngram in ENTERTAINING_ALLITERATIVE_NGRAMS:
        if word1.count(ngram) >= 1 and word2.count(ngram) >= 1:
            return True

    # Shares the same starting consonant
    if word1[0] in CONSONANTS and word2[0] == word1[0]:
        return True

    return False


def generate_random_words(prefixes: Set[str],
                          nouns: Set[str],
                          pleasing_fn=pleasing_combination,
                          timeout=timedelta(seconds=5)):

    # Search for a pleasing combination of words within a time limit
    time_limit = datetime.now() + timeout
    while datetime.now() < time_limit:
        prefix, = random.sample(prefixes, 1)

        for _ in range(1, 100):
            noun, = random.sample(nouns, 1)

            if pleasing_fn(prefix, noun):
                return f'{prefix}-{noun}'

    # If we can't find a pleasing combination within the time limit,
    # then we use any combination.
    prefix = random.sample(prefixes, 1)[0]
    noun = random.sample(nouns, 1)[0]

    return f'{prefix}-{noun}'


if __name__ == '__main__':
    regenerate_word_lists()
