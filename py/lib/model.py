import os
from typing import Type

from pynamodb import attributes as attributes
from pynamodb.constants import MAP
from pynamodb.models import Model

RECORDS_TABLE = os.environ['RECORDS_TABLE'] if 'RECORDS_TABLE' in os.environ else 'records'


class Claim(attributes.MapAttribute):
    owner = attributes.UnicodeAttribute()
    value = attributes.UnicodeAttribute()

    @staticmethod
    def of(owner: str, value: str):
        return Claim(owner=owner, value=value)


class TypedMapAttribute(attributes.Attribute, attributes.AttributeContainer):
    attr_type = MAP
    element_type = None

    def __init__(self, of: Type[attributes.MapAttribute], **atts):
        self.element_type = of
        super().__init__(**atts)

    def serialize(self, value):
        attribute = self.element_type()

        return {k: {'M': attribute.serialize(value[k])} for k in value}

    def deserialize(self, value):
        attribute = self.element_type()

        return {k: attribute.deserialize(value[k]['M']) for k in value}


class GroupModel(Model):
    class Meta:
        table_name = RECORDS_TABLE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = set() if self.values is None else self.values
        self.claims = dict() if self.claims is None else self.claims

    group = attributes.UnicodeAttribute(hash_key=True)
    values = attributes.UnicodeSetAttribute()
    claims = TypedMapAttribute(of=Claim)
    version = attributes.VersionAttribute()

    def claim(self, claim: Claim):
        owner = claim.owner
        requested_value = claim.value

        if owner in self.claims:
            # We accept an owner re-claim their pre-existing value, but do nothing.
            if self.claims[owner].value == requested_value:
                return
            # We reject one owner claiming multiple values.
            else:
                raise Exception(f'`{claim.owner}` can only claim one value')

        # We reject claiming a value that's already claimed by another owner
        if requested_value in self.values:
            raise Exception(f'`{claim.owner}` cannot claim `{requested_value}` as it is already claimed')

        self.values.add(requested_value)
        self.claims[claim.owner] = claim

    def disown(self, owner: str):
        # If the owner doesn't exist, nothing needs to happen.
        if owner not in self.claims:
            return

        old_value = self.claims[owner].value

        # Remove ownership of owned value
        self.values.remove(old_value)

        # Delete tracking for the owner.
        del self.claims[owner]

        return old_value
