import unittest
import unittest.mock as mock

from py.props import ResourcePropsDecoder
from py.resource_event_handler import ResourceEventHandler

CREATE_EVENT = {
    'RequestType': 'Create',
    'StackId': 'stack',
    'LogicalResourceId': 'resource',
    'ResourceProperties': {
        'Type': 'UUID',
        'Group': 'test',
    }
}

UPDATE_EVENT = {
    'RequestType': 'Update',
    'StackId': 'stack',
    'LogicalResourceId': 'resource',
    'ResourceProperties': {
        'Type': 'UUID',
        'Group': 'test',
    },
    'OldResourceProperties': {
        'Type': 'UUID',
        'Group': 'test2',
    }
}

DELETE_EVENT = {
    'RequestType': 'Delete',
    'StackId': 'stack',
    'LogicalResourceId': 'resource',
    'ResourceProperties': {
        'Type': 'UUID',
        'Group': 'test',
    }
}


class TestResourceEventHandler(unittest.TestCase):
    def test_create(self):
        handler = ResourceEventHandler()
        handler.allocator = mock.Mock(return_value='abcd')

        create_event = {
            'RequestType': 'Create',
            'StackId': 'stack',
            'LogicalResourceId': 'resource',
            'ResourceProperties': {
                'Type': 'UUID',
                'Group': 'test',
            }
        }

        expected_props = ResourcePropsDecoder().decode(create_event['ResourceProperties'])

        # WHEN
        handler.handle(create_event)

        # THEN
        handler.allocator.allocate.assert_called_with(expected_props, 'stack/resource')

    def test_update(self):
        handler = ResourceEventHandler()
        handler.allocator = mock.Mock(return_value='abcd')

        decoder = ResourcePropsDecoder()
        new_props = decoder.decode(UPDATE_EVENT['ResourceProperties'])
        old_props = decoder.decode(UPDATE_EVENT['OldResourceProperties'])

        # WHEN
        handler.handle(UPDATE_EVENT)

        # THEN
        handler.allocator.update.assert_called_with(old_props, new_props, 'stack/resource', 'stack/resource')

    def test_delete(self):
        handler = ResourceEventHandler()
        handler.allocator = mock.Mock(return_value='abcd')

        expected_props = ResourcePropsDecoder().decode(DELETE_EVENT['ResourceProperties'])

        # WHEN
        handler.handle(DELETE_EVENT)

        # THEN
        handler.allocator.deallocate.assert_called_with(expected_props, 'stack/resource')

    def test_delete_swallows_exception(self):
        handler = ResourceEventHandler()
        handler.allocator = mock.Mock()
        handler.allocator.deallocate = mock.Mock(side_effect=Exception('test'))

        expected_props = ResourcePropsDecoder().decode(DELETE_EVENT['ResourceProperties'])

        # WHEN
        handler.handle(DELETE_EVENT)

        # THEN
        handler.allocator.deallocate.assert_called_with(expected_props, 'stack/resource')
