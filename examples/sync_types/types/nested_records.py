from typing import TypedDict, Optional


class AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class OtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: AddressUSRecord
    other_thing: OtherThing
