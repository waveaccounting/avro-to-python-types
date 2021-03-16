from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import TypedDict, Optional
from uuid import UUID


class ExampleAvroAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    birthdate: date
    appt_date: date
    time_of_day_birth: time
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal
    address: ExampleAvroAddressUSRecord
