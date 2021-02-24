from typing import TypedDict, Optional


class ExampleAvroAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleAvroNextOtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class ExampleAvroOtherThing(TypedDict):
    thing1: str
    other_thing: ExampleAvroNextOtherThing


class ExampleAvroUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
    other_thing: ExampleAvroOtherThing
