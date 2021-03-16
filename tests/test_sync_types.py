from fastavro import writer, reader, parse_schema
from datetime import date, time, datetime, timezone
from uuid import UUID
from decimal import Decimal
from typing import TypedDict, Optional
import snapshottest


nested_record_schema = {
    "namespace": "example.avro",
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "favorite_number", "type": ["null", "int"]},
        {"name": "favorite_color", "type": ["null", "string"]},
        {"name": "birthdate", "type": {"type": "int", "logicalType": "date"}},
        {"name": "appt_date", "type": {"type": "int", "logicalType": "date"}},
        {
            "name": "time_of_day_birth",
            "type": {"type": "int", "logicalType": "time-millis"},
        },
        {
            "name": "timestamp_of_birth",
            "type": {"type": "long", "logicalType": "timestamp-millis"},
        },
        {
            "name": "uuid_of_birth_record",
            "type": {"type": "string", "logicalType": "uuid"},
        },
        {
            "name": "weight",
            "type": {
                "type": "bytes",
                "logicalType": "decimal",
                "precision": 5,
                "scale": 2,
            },
        },
        {
            "name": "address",
            "type": {
                "type": "record",
                "name": "AddressUSRecord",
                "fields": [
                    {"name": "streetaddress", "type": "string"},
                    {"name": "city", "type": "string"},
                ],
            },
        },
    ],
}


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


class SnapshotTestSyncedTypes(snapshottest.TestCase):
    def test_synced_types(self):
        """The nested_record_schema was parsed using this package to create the concrete class 'ExampleAvroUser' above.
        This test uses fastavro to serialize ExampleAvroUser and then deserialize it and compares the result to
        a snapshot.
            Note: that the datetime fields have utc time zones associated with them because the datetime package
            assumes that if the timezone is not provided it is local, however the fastavro package will default it
            to utc when when serializing it.  So if you serialize and deserialize something with a 'niave' datetime
            variable the resulting value will not match the original and will differ by your offset from utc.
            Worse still if you serialize such a variable in one timezone and deserialize it in another the results will not
            differ by the same amount!  Thus defeating any local adjustment you had in place.  This could be serious for
            code that runs accross AWS regions.
        """
        self.maxDiff = None
        parsed_schema = parse_schema(nested_record_schema)
        records: list(ExampleAvroUser) = [
            {
                "name": "walter",
                "favorite_number": 41,
                "favorite_color": "cyan",
                "birthdate": date(1989, 1, 11),
                "appt_date": date(1993, 4, 21),
                "time_of_day_birth": time(12, 21, 45, 3456),
                "timestamp_of_birth": datetime(
                    1989, 1, 11, 1, 21, 45, tzinfo=timezone.utc
                ),
                "uuid_of_birth_record": "e6a848a6-2682-4e9c-afe2-895f9bd45ff8",
                "weight": Decimal(12.55).__round__(2),
                "address": {
                    "streetaddress": "154 Sparkling Heaven Dr",
                    "city": "bergsville",
                },
            },
            {
                "name": "george",
                "favorite_number": 666,
                "favorite_color": "red",
                "birthdate": date(1999, 1, 11),
                "appt_date": date(1993, 2, 21),
                "time_of_day_birth": time(4, 21, 45, 5678),
                "timestamp_of_birth": datetime(
                    1999, 2, 11, 2, 22, 45, tzinfo=timezone.utc
                ),
                "uuid_of_birth_record": "6c6a29f9-185e-476f-8055-ec91530ee561",
                "weight": Decimal(44.55).__round__(2),
                "address": {"streetaddress": "1 Bowling Lawn Green", "city": "Dulock"},
            },
            {
                "name": "marie",
                "favorite_number": 92,
                "favorite_color": "black",
                "birthdate": date(1911, 1, 11),
                "appt_date": date(1944, 4, 21),
                "time_of_day_birth": time(1, 13, 37, 9878),
                "timestamp_of_birth": datetime(
                    1989, 1, 11, 3, 21, 45, tzinfo=timezone.utc
                ),
                "uuid_of_birth_record": "6c6a29f9-185e-476f-8055-ec91530ee561",
                "weight": Decimal(26.3).__round__(2),
                "address": {
                    "streetaddress": "66 Springfield Cr",
                    "city": "Springfield",
                },
            },
        ]

        with open(f"/tmp/nested_type.avro", "wb") as message_out:
            writer(message_out, parsed_schema, records)

        with open(f"/tmp/nested_type.avro", "rb") as message_in:
            i = 1
            for record in reader(message_in):
                self.assertMatchSnapshot(record, name=f"test_synced_types{i}")
                i += 1
