from typing import TypedDict, Optional

class ExampleAvroAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
