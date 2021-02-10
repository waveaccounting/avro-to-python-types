# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildA.avsc'] = '''from typing import TypedDict, Optional

class common_ChildA(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildB.avsc'] = '''from typing import TypedDict, Optional

class common_ChildB(TypedDict):
    streetaddress: str
    city: str
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas domain.Parent.avsc'] = '''from typing import TypedDict, Optional

class common_ChildA(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]


class common_ChildB(TypedDict):
    streetaddress: str
    city: str


class domain_CompositeItem(TypedDict):
    composite_a: common_ChildA
    composite_b: common_ChildB


class domain_Parent(TypedDict):
    first_item: common_ChildA
    second_item: common_ChildA
    composite_item: domain_CompositeItem
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_record.avsc'] = '''from typing import TypedDict, Optional

class example_avro_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_avro_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_avro_AddressUSRecord
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_records.avsc'] = '''from typing import TypedDict, Optional

class example_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_OtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class example_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_AddressUSRecord
    other_thing: example_OtherThing
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_records_deep.avsc'] = '''from typing import TypedDict, Optional

class example_avro_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_avro_NextOtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class example_avro_OtherThing(TypedDict):
    thing1: str
    other_thing: example_avro_NextOtherThing


class example_avro_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_avro_AddressUSRecord
    other_thing: example_avro_OtherThing
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_record.avsc'] = '''from typing import TypedDict, Optional

class example_avro_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_avro_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_avro_AddressUSRecord
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_records.avsc'] = '''from typing import TypedDict, Optional

class example_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_OtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class example_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_AddressUSRecord
    other_thing: example_OtherThing
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_records_deep.avsc'] = '''from typing import TypedDict, Optional

class example_avro_AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class example_avro_NextOtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class example_avro_OtherThing(TypedDict):
    thing1: str
    other_thing: example_avro_NextOtherThing


class example_avro_User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: example_avro_AddressUSRecord
    other_thing: example_avro_OtherThing
'''
