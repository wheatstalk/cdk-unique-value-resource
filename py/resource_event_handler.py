import json
import logging

from pynamodb.connection import Connection

from py.lib.allocator import UniqueValueAllocator
from py.props import ResourcePropsDecoder


def swallow_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.warning(f'Unhandled exception: {e}')
            return format_unique_value_response(str(e))

    return wrapper


class ResourceEventHandler:
    props_decoder: ResourcePropsDecoder = ResourcePropsDecoder()
    allocator = UniqueValueAllocator(connection=Connection())

    def handle(self, event):
        request_type = extract_request_type(event)
        owner = extract_owner(event)

        if request_type == 'Create':
            return self.on_create(owner, event)
        elif request_type == 'Update':
            return self.on_update(owner, event)
        elif request_type == 'Delete':
            return self.on_delete(owner, event)
        else:
            raise Exception(f'Unknown request type {request_type}')

    def on_create(self, owner: str, event):
        props = self.props_decoder.decode(event['ResourceProperties'])
        unique_value = self.allocator.allocate(props, owner)

        return format_unique_value_response(unique_value)

    def on_update(self, owner: str, event):
        old_props = self.props_decoder.decode(event['OldResourceProperties'])
        new_props = self.props_decoder.decode(event['ResourceProperties'])

        unique_value = self.allocator.update(old_props, new_props, owner, owner)

        return format_unique_value_response(unique_value)

    @swallow_exceptions
    def on_delete(self, owner: str, event):
        props = self.props_decoder.decode(event['ResourceProperties'])
        self.allocator.deallocate(props, owner)


def format_unique_value_response(unique_value):
    return {
        'Data': {
            'UniqueValue': unique_value,
        },
    }


def extract_request_type(event: dict):
    return event['RequestType']


def extract_owner(event: dict):
    stack_id = event['StackId']
    logical_resource_id = event['LogicalResourceId']
    physical_resource_id = f'{stack_id}/{logical_resource_id}'

    return physical_resource_id


def on_event(event, context):
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f'event = {json.dumps(event)}')
    return ResourceEventHandler().handle(event)