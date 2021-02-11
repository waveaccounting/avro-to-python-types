from typing import TypedDict, Optional


class example_avro_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_avro_OtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class example_avro_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_avro_AddressUSRecord
    other_thing: example_avro_OtherThing
