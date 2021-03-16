# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildA.avsc'] = '''from typing import TypedDict, Optional


class CommonChildA(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildB.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import TypedDict, Optional
from uuid import UUID


class CommonChildB(TypedDict):
    streetaddress: str
    city: str
    birthdate: date
    appt_date: date
    time_of_day_birth: time
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildC.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import TypedDict, Optional
from uuid import UUID


class CommonChildB(TypedDict):
    streetaddress: Optional[str]
    city: Optional[str]
    birthdate: date
    appt_date: date
    time_of_day_birth: Optional[time]
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas domain.Parent.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import TypedDict, Optional
from uuid import UUID


class CommonChildA(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]


class CommonChildB(TypedDict):
    streetaddress: str
    city: str
    birthdate: date
    appt_date: date
    time_of_day_birth: time
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal


class DomainCompositeItem(TypedDict):
    composite_a: CommonChildA
    composite_b: CommonChildB


class DomainParent(TypedDict):
    first_item: CommonChildA
    second_item: CommonChildA
    composite_item: DomainCompositeItem
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_record.avsc'] = '''from typing import TypedDict, Optional


class ExampleAvroAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_records.avsc'] = '''from typing import TypedDict, Optional


class ExampleAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleOtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class ExampleUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAddressUSRecord
    other_thing: ExampleOtherThing
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_records_deep.avsc'] = '''from typing import TypedDict, Optional


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
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_record.avsc'] = '''from typing import TypedDict, Optional


class ExampleAvroAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_records.avsc'] = '''from typing import TypedDict, Optional


class ExampleAddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class ExampleOtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class ExampleUser(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAddressUSRecord
    other_thing: ExampleOtherThing
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_records_deep.avsc'] = '''from typing import TypedDict, Optional


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
'''
