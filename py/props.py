from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class UniqueIntegerProps:
    Start: int
    Stop: int
    Step: int = 1


@dataclass
class UUIDProps:
    Version: str = 'UUID4'
    Namespace: Optional[uuid.UUID] = uuid.NAMESPACE_URL
    Name: Optional[str] = 'group'

    UUID1 = 'UUID1'
    UUID4 = 'UUID4'

    def is_uuid1(self):
        return self.Version == self.UUID1

    def is_uuid4(self):
        return self.Version == self.UUID4


@dataclass
class ResourceProps:
    Type: str
    Group: str
    UniqueInteger: Optional[UniqueIntegerProps] = None
    UUID: Optional[UUIDProps] = None
    # Filled by CloudFormation
    ServiceToken: Optional[str] = None

    TYPE_UNIQUE_INTEGER = 'UniqueInteger'
    TYPE_UUID = 'UUID'
    TYPE_UNIQUE_WORDS = 'UniqueWords'


class ResourcePropsDecoder:
    def decode(self, props: dict):
        props = dict(props)
        resource_type = props['Type']

        if resource_type == ResourceProps.TYPE_UNIQUE_INTEGER:
            unique_integer_props = dict(props['UniqueInteger'])

            for name in ['Start', 'Stop', 'Step']:
                if name in unique_integer_props:
                    unique_integer_props[name] = int(unique_integer_props[name])

            props['UniqueInteger'] = UniqueIntegerProps(**unique_integer_props)

        elif resource_type == ResourceProps.TYPE_UUID:
            uuid_props = dict(props['UUID']) if 'UUID' in props else dict()

            if 'Namespace' in uuid_props:
                uuid_props['Namespace'] = uuid.UUID(uuid_props['Namespace'])

            props['UUID'] = UUIDProps(**uuid_props)

        elif resource_type == ResourceProps.TYPE_UNIQUE_WORDS:
            pass

        else:
            raise Exception(f'Invalid resource type {resource_type}')

        return ResourceProps(**props)
