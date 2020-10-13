import re
import unittest

from py.lib.random_words import generate_random_words, get_word_lists, regenerate_word_lists


class TestRandomWords(unittest.TestCase):
    def test_get_word_lists(self):
        verbs, nouns = get_word_lists()

        self.assertGreater(len(verbs), 1000)
        self.assertGreater(len(nouns), 1000)
        self.assertIn('overemphasized', verbs)
        self.assertIn('specifics', nouns)

        domain_friendly = re.compile(r'^[a-z][a-z0-9]*$')
        for word in verbs.union(nouns):
            self.assertTrue(domain_friendly.match(word))

    def xtest_generate_word_lists(self):
        regenerate_word_lists()

    def test_generate_random_words(self):
        verbs, nouns = get_word_lists()
        names = [generate_random_words(verbs, nouns) for _ in range(0, 100)]
        names_unique = set(names)

        self.assertGreaterEqual(len(names_unique) / len(names), 0.7, msg='expected 70% of names to be unique')

        for name in names:
            print(name)
            self.assertGreater(len(name), 0)
