import unittest

from pynamodb.connection import Connection

from py.lib.allocator import UniqueValueAllocator
from py.lib.model import GroupModel
from py.props import ResourceProps, UniqueIntegerProps

LOCAL_STACK_HOST = 'http://localhost:4566'


class TestAllocator(unittest.TestCase):
    def setUp(self):
        self.connection = Connection(host=LOCAL_STACK_HOST)
        GroupModel.Meta.host = LOCAL_STACK_HOST

        if GroupModel.exists():
            GroupModel.delete_table()

        GroupModel.create_table(billing_mode='PAY_PER_REQUEST')

    def tearDown(self):
        GroupModel.delete_table()

    def test_allocation(self):
        # GIVEN
        props = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_INTEGER,
                              Group='uniqueints',
                              UniqueInteger=UniqueIntegerProps(Start=10000, Stop=40000))
        allocator = UniqueValueAllocator(self.connection)

        # WHEN
        first = allocator.allocate(props, 'me')
        second = allocator.allocate(props, 'other')

        # THEN
        # Allocated values are unique
        self.assertNotEqual(first, second)

        # Allocated values are in the group model's list of values.
        group_model = GroupModel.get(allocator.group_name(props))

        self.assertEqual(2, len(group_model.values))
        self.assertIn(first, group_model.values)
        self.assertIn(second, group_model.values)

    def test_deallocation(self):
        # GIVEN
        props = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_INTEGER,
                              Group='uniqueints',
                              UniqueInteger=UniqueIntegerProps(Start=10000, Stop=40000))
        allocator = UniqueValueAllocator(self.connection)
        allocator.allocate(props, 'me')

        # WHEN
        allocator.deallocate(props, 'me')

        # THEN
        group_model = GroupModel.get(allocator.group_name(props))

        self.assertEqual(set(), group_model.values)

    def test_allocation_update_within_group(self):
        # GIVEN
        props = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_INTEGER,
                              Group='uniqueints',
                              UniqueInteger=UniqueIntegerProps(Start=10000, Stop=40000))

        group = props.Group
        allocator = UniqueValueAllocator(self.connection)
        original_unique = allocator.allocate(props, 'me')

        # WHEN
        updated_unique = allocator.update(from_props=props, to_props=props, from_owner='me', to_owner='me2')

        # THEN
        group_model = GroupModel.get(allocator.group_name(props))
        self.assertEqual(original_unique, updated_unique)
        self.assertEqual({updated_unique}, group_model.values)

    def test_allocation_update_outside_group(self):
        # GIVEN
        props_a = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_INTEGER,
                                Group='group-a',
                                UniqueInteger=UniqueIntegerProps(Start=10000, Stop=40000))

        props_b = ResourceProps(Type=ResourceProps.TYPE_UNIQUE_INTEGER,
                                Group='group-b',
                                UniqueInteger=UniqueIntegerProps(Start=10000, Stop=40000))

        allocator = UniqueValueAllocator(self.connection)

        owner = 'me'
        allocator.allocate(props_a, owner)

        # WHEN
        updated_unique = allocator.update(from_props=props_a, to_props=props_b, from_owner=owner, to_owner=owner)

        # THEN
        group_model_a = GroupModel.get(allocator.group_name(props_a))
        self.assertEqual(set(), group_model_a.values)
        group_model_b = GroupModel.get(allocator.group_name(props_b))
        self.assertEqual({updated_unique}, group_model_b.values)
