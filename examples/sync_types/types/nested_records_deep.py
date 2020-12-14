from typing import TypedDict, Optional


class AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class NextOtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class OtherThing(TypedDict):
    thing1: str
    other_thing: NextOtherThing


class User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: AddressUSRecord
    other_thing: OtherThing
