import unittest

from py.lib.generator import UniqueIntegerGenerator, UniqueValueExhaustion, UUIDGenerator, get_generator, \
    UniqueWordsGenerator
from py.props import UUIDProps, ResourceProps, UniqueIntegerProps


class TestUnique(unittest.TestCase):
    def test_selects_unique_int_generator(self):
        # GIVEN
        props = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_INTEGER,
                              Group='uniqueints',
                              UniqueInteger=UniqueIntegerProps(Start=10000, Stop=40000))

        # WHEN
        generator = get_generator(props)

        # THEN
        self.assertIsInstance(generator, UniqueIntegerGenerator)

    def test_selects_uuid_generator(self):
        # GIVEN
        props = ResourceProps(Type=ResourceProps.TYPE_UUID, Group='uuids')

        # WHEN
        generator = get_generator(props)

        # THEN
        self.assertIsInstance(generator, UUIDGenerator)

    def test_selects_random_words_generator(self):
        # GIVEN
        props = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_WORDS, Group='words')

        # WHEN
        generator = get_generator(props)

        # THEN
        self.assertIsInstance(generator, UniqueWordsGenerator)

    def test_unique(self):
        u = UniqueIntegerGenerator(range(1, 10))
        self.assertEqual(9, u.generate_with_ints(set(range(1, 9))))
        self.assertEqual(1, u.generate_with_ints(set(range(2, 10))))

    def test_exhaustion(self):
        r = range(1, 10)
        u = UniqueIntegerGenerator(r)

        with self.assertRaises(UniqueValueExhaustion):
            u.generate_with_ints(set(r))

    def test_uuid(self):
        for v in [UUIDProps.UUID1, UUIDProps.UUID4]:
            uuid_props = UUIDProps(Version=v)
            generator = UUIDGenerator(props=uuid_props)
            generated = generator.generate(set())
            generated2 = generator.generate(set())
            self.assertRegex(generated, r'^[0-9a-f]{8}')
            self.assertNotEqual(generated, generated2)

    def test_random_words(self):
        # GIVEN
        generator = UniqueWordsGenerator()
        words = set()

        # WHEN
        words.add(generator.generate(words))
        words.add(generator.generate(words))

        # THEN
        self.assertEqual(2, len(words))
