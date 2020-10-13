import unittest

from py.lib.model import GroupModel, Claim, TypedMapAttribute


class TestModel(unittest.TestCase):
    def test_typed_map_attribute(self):
        att = TypedMapAttribute(of=Claim)
        record = {
            'me': {
                'M': {
                    'owner': {
                        'S': 'me'
                    },
                    'value': {
                        'S': '1'
                    }
                }
            },
            'me2': {
                'M': {
                    'owner': {
                        'S': 'me2'
                    },
                    'value': {
                        'S': ['2']
                    }
                }
            },
        }

        # WHEN
        deserialized = att.deserialize(record)
        serialized = att.serialize(deserialized)

        # THEN
        self.assertIsInstance(deserialized, dict)
        self.assertIsInstance(deserialized['me'], Claim)
        self.assertIsInstance(deserialized['me2'], Claim)
        self.assertEqual(record, serialized)

    def test_claims(self):
        model = GroupModel()
        model.claim(Claim.of('a', 'value-a'))
        model.claim(Claim.of('b', 'value-b'))
        self.assertEqual(sorted(model.values), ['value-a', 'value-b'])

    def test_accepting_same_owner_reclaims_same_value(self):
        # GIVEN
        model = GroupModel()

        # WHEN
        model.claim(Claim.of('a', 'value-a'))
        model.claim(Claim.of('a', 'value-a'))

        # THEN
        self.assertEqual(sorted(model.values), ['value-a'])

    def test_rejecting_claiming_several(self):
        # GIVEN
        model = GroupModel()
        model.claim(Claim.of('a', 'value'))

        # WHEN / THEN
        with self.assertRaisesRegex(Exception, r'claim one'):
            model.claim(Claim.of('a', 'value2'))

    def test_rejecting_claiming_owned_value(self):
        # GIVEN
        model = GroupModel()
        model.claim(Claim.of('a', 'value'))

        # WHEN / THEN
        with self.assertRaisesRegex(Exception, r'cannot claim'):
            model.claim(Claim.of('b', 'value'))

    def test_disowning(self):
        # GIVEN
        model = GroupModel()
        model.claim(Claim.of('a', 'value-a'))
        model.claim(Claim.of('b', 'value-b'))

        # WHEN
        model.disown('a')

        # THEN
        self.assertEqual({'value-b'}, model.values)

    def test_disowning_nonexistent(self):
        # GIVEN
        model = GroupModel()
        model.claim(Claim.of('a', 'value-a'))

        # WHEN
        model.disown('b')

        # THEN
        self.assertEqual({'value-a'}, model.values)
