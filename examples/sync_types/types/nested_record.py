from typing import TypedDict, Optional


class AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: AddressUSRecord
