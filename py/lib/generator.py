from typing import Set
import uuid

from py.lib.random_words import get_word_lists, generate_random_words
from py.props import UUIDProps, ResourceProps


class UniqueValueGenerator:
    def generate(self, unavailable: Set[str]) -> str:
        pass

    def group_name(self, props: ResourceProps):
        return props.Group


class UniqueValueExhaustion(Exception):
    pass


class UniqueIntegerGenerator(UniqueValueGenerator):
    range: range

    def __init__(self, r):
        self.range = r

    def generate(self, unavailable: Set[str]) -> str:
        unavailable_ints = {int(f) for f in unavailable}
        generated_int = self.generate_with_ints(unavailable_ints)
        return str(generated_int)

    def generate_with_ints(self, unavailable: Set[int]) -> int:
        for n in self.range:
            if n not in unavailable:
                return n

        raise UniqueValueExhaustion(f'There are no unique integers left in the range {self.range}')

    def group_name(self, props: ResourceProps):
        return f'{props.Group}:UniqueInteger'


class UUIDGenerator(UniqueValueGenerator):
    props: UUIDProps

    def __init__(self, props: UUIDProps):
        self.props = props

    def generate(self, _unavailable: Set[str]):
        return str(generate_uuid(self.props))

    def group_name(self, props: ResourceProps):
        return f'{props.Group}:{self.props.Version}'


def generate_uuid(props: UUIDProps):
    if props.is_uuid1():
        return uuid.uuid1()
    elif props.is_uuid4():
        return uuid.uuid4()


class UniqueWordsGenerator(UniqueValueGenerator):
    verbs: Set[str]
    nouns: Set[str]

    def __init__(self):
        self.verbs, self.nouns = get_word_lists()

    def generate(self, unavailable: Set[str]) -> str:
        for _ in range(0, 10):
            name = generate_random_words(self.verbs, self.nouns)
            if name not in unavailable:
                return name

        raise UniqueValueExhaustion('Seem to have used up available random words')

    def group_name(self, props: ResourceProps):
        return f'{props.Group}:RandomWords'


def get_generator(props: ResourceProps) -> UniqueValueGenerator:
    if props.Type == props.TYPE_UNIQUE_INTEGER:
        start = props.UniqueInteger.Start
        stop = props.UniqueInteger.Stop
        step = props.UniqueInteger.Step

        return UniqueIntegerGenerator(range(start, stop, step))

    elif props.Type == props.TYPE_UUID:
        return UUIDGenerator(props.UUID)

    elif props.Type == props.TYPE_UNIQUE_WORDS:
        return UniqueWordsGenerator()

    raise Exception(f'Unknown prop type {props.Type}')