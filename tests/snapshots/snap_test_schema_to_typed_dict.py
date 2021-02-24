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

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildB.avsc'] = '''from typing import TypedDict, Optional

class CommonChildB(TypedDict):
    streetaddress: str
    city: str
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas domain.Parent.avsc'] = '''from typing import TypedDict, Optional

class CommonChildA(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]


class CommonChildB(TypedDict):
    streetaddress: str
    city: str


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
