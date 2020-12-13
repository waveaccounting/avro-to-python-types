# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "SnapshotSchemaToTypedDict::test_snapshot_all_schemas nested_record.avsc"
] = """from typing import TypedDict, Optional

class AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: AddressUSRecord
"""

snapshots[
    "SnapshotSchemaToTypedDict::test_snapshot_all_schemas nested_records.avsc"
] = """from typing import TypedDict, Optional

class AddressUSRecord(TypedDict):
    streetaddress: str
    city: str


class OtherThing(TypedDict):
    thing1: str
    thing2: Optional[int]


class User(TypedDict):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: AddressUSRecord
    other_thing: OtherThing
"""
