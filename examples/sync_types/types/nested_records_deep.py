from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroNextOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleAvroOtherThing(TypedDict, total=False):
    thing1: str
    other_thing: ExampleAvroNextOtherThing


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
    other_thing: ExampleAvroOtherThing
