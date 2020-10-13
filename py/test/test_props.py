import unittest
import uuid

from py.props import ResourcePropsDecoder, UniqueIntegerProps, UUIDProps


class TestProps(unittest.TestCase):
    def test_uuid(self):
        # GIVEN
        props = {'Type': 'UUID', 'Group': 'test'}

        # WHEN
        uuid_props = ResourcePropsDecoder().decode(props)

        # THEN
        self.assertEqual('UUID', uuid_props.Type)
        self.assertIsInstance(uuid_props.UUID, UUIDProps)
        self.assertEqual(UUIDProps.UUID4, uuid_props.UUID.Version)
        self.assertEqual(uuid.NAMESPACE_URL, uuid_props.UUID.Namespace)
        self.assertEqual('group', uuid_props.UUID.Name)

    def test_uuid_specified(self):
        # GIVEN
        unique = {
            'Type': 'UUID',
            'Group': 'test',
            'UUID': {
                'Version': 'UUID1',
                'Namespace': '6ba7b814-9dad-11d1-80b4-00c04fd430c8',
                'Name': 'foobar',
            }
        }

        # WHEN
        uuid_props = ResourcePropsDecoder().decode(unique)

        # THEN
        self.assertIsInstance(uuid_props.UUID, UUIDProps)
        self.assertEqual(UUIDProps.UUID1, uuid_props.UUID.Version)
        self.assertEqual(uuid.UUID('6ba7b814-9dad-11d1-80b4-00c04fd430c8'), uuid_props.UUID.Namespace)
        self.assertEqual('foobar', uuid_props.UUID.Name)

    def test_unique_integer(self):
        # GIVEN
        unique = {
            'Type': 'UniqueInteger',
            'Group': 'test',
            'UniqueInteger': {
                'Start': 1000,
                'Stop': 10000,
                'Step': 10,
            }
        }

        # WHEN
        unique_integer_props = ResourcePropsDecoder().decode(unique)

        # THEN
        self.assertEqual('UniqueInteger', unique_integer_props.Type)
        self.assertIsInstance(unique_integer_props.UniqueInteger, UniqueIntegerProps)
        self.assertEqual(unique_integer_props.UniqueInteger.Start, 1000)
        self.assertEqual(unique_integer_props.UniqueInteger.Stop, 10000)
        self.assertEqual(unique_integer_props.UniqueInteger.Step, 10)

    def test_unique_integer_default_step(self):
        # GIVEN
        unique = {
            'Type': 'UniqueInteger',
            'Group': 'test',
            'UniqueInteger': {
                'Start': 1000,
                'Stop': 10000,
            }
        }

        # WHEN
        unique_integer_props = ResourcePropsDecoder().decode(unique)

        # THEN
        self.assertEqual(unique_integer_props.UniqueInteger.Step, 1)

    def test_unknown_type(self):
        # GIVEN
        unknown = {'Type': 'UNKNOWN', 'Group': 'test'}

        # WHEN
        with self.assertRaisesRegex(Exception, r'Invalid'):
            ResourcePropsDecoder().decode(unknown)
