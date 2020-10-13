from typing import Any

from pynamodb.connection import Connection
from pynamodb.transactions import TransactGet, TransactWrite

from py.lib.model import GroupModel, Claim
from py.lib.optimistic import optimistic_retry
from py.lib.generator import get_generator
from py.props import ResourceProps


class UniqueValueAllocator:
    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    @optimistic_retry
    def allocate(self, props: ResourceProps, owner: str):
        generator = get_generator(props)

        group = generator.group_name(props)

        with TransactGet(self.connection) as t:
            group_model_future: Any = t.get(GroupModel, group)

        group_model = resolve_or_create(group_model_future, group)

        unique = generator.generate(group_model.values)

        group_model.claim(Claim.of(owner, unique))
        group_model.save()

        return unique

    @optimistic_retry
    def deallocate(self, props: ResourceProps, owner: str):
        group = get_generator(props).group_name(props)

        with TransactGet(connection=self.connection) as t:
            model_future: Any = t.get(GroupModel, group)

        group_model = model_future.get()
        group_model.disown(owner)
        group_model.save()

    @optimistic_retry
    def update(self, from_props: ResourceProps, to_props: ResourceProps, from_owner: str, to_owner: str):
        from_generator = get_generator(from_props)
        from_group = from_generator.group_name(from_props)

        to_generator = get_generator(to_props)
        to_group = to_generator.group_name(to_props)

        if from_group == to_group and from_owner != to_owner:
            # When it's the same group, but different owner, transfer the value
            # over.
            with TransactGet(connection=self.connection) as t:
                model_future: Any = t.get(GroupModel, from_group)

            group_model = resolve_or_create(model_future, from_group)

            unique_value = group_model.disown(from_owner)
            # Re-use the unique value belonging to the old owner.
            group_model.claim(Claim.of(to_owner, unique_value))
            group_model.save()

            return unique_value

        else:
            with TransactGet(connection=self.connection) as t:
                from_model_future: Any = t.get(GroupModel, from_group)
                to_model_future: Any = t.get(GroupModel, to_group)

            from_group_model = resolve_or_create(from_model_future, from_group)
            to_group_model = resolve_or_create(to_model_future, to_group)

            with TransactWrite(connection=self.connection) as t:
                from_group_model.disown(from_owner)
                t.save(from_group_model)

                unique = to_generator.generate(to_group_model.values)
                to_group_model.claim(Claim.of(to_owner, unique))
                t.save(to_group_model)

                return unique

    def group_name(self, props: ResourceProps):
        return get_generator(props).group_name(props)


def resolve_or_create(model_future, group):
    try:
        new_group_model = model_future.get()
    except GroupModel.DoesNotExist:
        new_group_model = GroupModel(group=group)
    return new_group_model
