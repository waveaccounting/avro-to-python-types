from typing import TypedDict, Optional


class example_avro_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_avro_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_avro_AddressUSRecord
