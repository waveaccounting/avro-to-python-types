# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SnapshotTypedDictArrayFromSchemaFile::test_array_map_schemas com.wave.Order.avsc'] = '''from enum import Enum
from typing import TypedDict


class ComWaveProduct_status(Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    ONLY_FEW_LEFT = "ONLY_FEW_LEFT"


class ComWaveProduct(TypedDict, total=False):
    product_id: int
    product_name: str
    product_description: Optional[str]
    product_status: ComWaveProduct_status
    product_category: list(str)
    price: float
    product_hash: str


class ComWaveOrderDetail(TypedDict, total=False):
    quantity: int
    total: float
    product_detail: ComWaveProduct


class ComWaveOrder(TypedDict, total=False):
    order_id: int
    customer_id: int
    total: float
    order_details: list(ComWaveOrderDetail)
'''

snapshots['SnapshotTypedDictArrayFromSchemaFile::test_array_map_schemas com.wave.OrderDetail.avsc'] = '''from enum import Enum
from typing import TypedDict


class ComWaveProduct_status(Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    ONLY_FEW_LEFT = "ONLY_FEW_LEFT"


class ComWaveProduct(TypedDict, total=False):
    product_id: int
    product_name: str
    product_description: Optional[str]
    product_status: ComWaveProduct_status
    product_category: list(str)
    price: float
    product_hash: str


class ComWaveOrderDetail(TypedDict, total=False):
    quantity: int
    total: float
    product_detail: ComWaveProduct
'''

snapshots['SnapshotTypedDictArrayFromSchemaFile::test_array_map_schemas com.wave.Product.avsc'] = '''from enum import Enum
from typing import Optional, TypedDict


class ComWaveProduct_status(Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    ONLY_FEW_LEFT = "ONLY_FEW_LEFT"


class ComWaveProduct(TypedDict, total=False):
    product_id: int
    product_name: str
    product_description: Optional[str]
    product_status: ComWaveProduct_status
    product_category: list(str)
    price: float
    product_hash: str
'''

snapshots['SnapshotTypedDictArrayFromSchemaFile::test_array_map_schemas wave_arraytype.avsc'] = '''from typing import Optional, TypedDict


class WavePytestArrayUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictArrayMapFromSchemaFile::test_array_map_schemas com.wave.Order.avsc'] = '''from typing import TypedDict


class ComWaveOrder(TypedDict, total=False):
    order_id: int
    customer_id: int
    total: float
    order_details: array
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_expandable_schemas common.ChildA.avsc'] = '''from typing import Optional, TypedDict


class CommonChildA(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_expandable_schemas common.ChildB.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import TypedDict
from uuid import UUID


class CommonChildB(TypedDict, total=False):
    streetaddress: str
    city: str
    birthdate: date
    appt_date: date
    time_of_day_birth: time
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_expandable_schemas common.ChildC.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from enum import Enum
from typing import Optional, TypedDict
from uuid import UUID


class CommonSchool(Enum):
    StBonifice = StBonifice
    HogWarts = HogWarts
    HardKnocks = HardKnocks
    UnseenUniversity = UnseenUniversity


class CommonEyeColor(Enum):
    green = green
    brown = brown
    blue = blue


class CommonChildC(TypedDict, total=False):
    streetaddress: Optional[str]
    city: Optional[str]
    birthdate: date
    appt_date: date
    time_of_day_birth: Optional[time]
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal
    timestamp_of_first_checkup: Optional[datetime]
    school: CommonSchool
    eyeclolor: Optional[CommonEyeColor]
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_expandable_schemas domain.Parent.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import Optional, TypedDict
from uuid import UUID


class CommonChildA(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]


class CommonChildB(TypedDict, total=False):
    streetaddress: str
    city: str
    birthdate: date
    appt_date: date
    time_of_day_birth: time
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal


class DomainCompositeItem(TypedDict, total=False):
    composite_a: CommonChildA
    composite_b: CommonChildB


class DomainParent(TypedDict, total=False):
    first_item: CommonChildA
    second_item: CommonChildA
    composite_item: DomainCompositeItem
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_self_contained_schemas nested_record.avsc'] = '''from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_self_contained_schemas nested_records.avsc'] = '''from typing import Optional, TypedDict


class ExampleAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAddressUSRecord
    other_thing: ExampleOtherThing
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_self_contained_schemas nested_records_deep.avsc'] = '''from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroNextOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleAvroOtherThing(TypedDict, total=False):
    thing1: str
    other_thing: ExampleAvroNextOtherThing


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
    other_thing: ExampleAvroOtherThing
'''

snapshots['SnapshotTypedDictFromOrder::test_snapshot_self_contained_schemas no_optional_field_record.avsc'] = '''from typing import TypedDict


class ExampleAvroAnotherExample(TypedDict, total=False):
    id: str
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildA.avsc'] = '''from typing import Optional, TypedDict


class CommonChildA(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas common.ChildB.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import TypedDict
from uuid import UUID


class CommonChildB(TypedDict, total=False):
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
from enum import Enum
from typing import Optional, TypedDict
from uuid import UUID


class CommonSchool(Enum):
    StBonifice = StBonifice
    HogWarts = HogWarts
    HardKnocks = HardKnocks
    UnseenUniversity = UnseenUniversity


class CommonEyeColor(Enum):
    green = green
    brown = brown
    blue = blue


class CommonChildC(TypedDict, total=False):
    streetaddress: Optional[str]
    city: Optional[str]
    birthdate: date
    appt_date: date
    time_of_day_birth: Optional[time]
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal
    timestamp_of_first_checkup: Optional[datetime]
    school: CommonSchool
    eye_color: Optional[CommonEyeColor]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_expandable_schemas domain.Parent.avsc'] = '''from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import Optional, TypedDict
from uuid import UUID


class CommonChildA(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]


class CommonChildB(TypedDict, total=False):
    streetaddress: str
    city: str
    birthdate: date
    appt_date: date
    time_of_day_birth: time
    timestamp_of_birth: datetime
    uuid_of_birth_record: UUID
    weight: Decimal


class DomainCompositeItem(TypedDict, total=False):
    composite_a: CommonChildA
    composite_b: CommonChildB


class DomainParent(TypedDict, total=False):
    first_item: CommonChildA
    second_item: CommonChildA
    composite_item: DomainCompositeItem
    favorite_color: Optional[str]
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_record.avsc'] = '''from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_records.avsc'] = '''from typing import Optional, TypedDict


class ExampleAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAddressUSRecord
    other_thing: ExampleOtherThing
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas nested_records_deep.avsc'] = '''from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroNextOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleAvroOtherThing(TypedDict, total=False):
    thing1: str
    other_thing: ExampleAvroNextOtherThing


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
    other_thing: ExampleAvroOtherThing
'''

snapshots['SnapshotTypedDictFromSchemaFile::test_snapshot_self_contained_schemas no_optional_field_record.avsc'] = '''from typing import TypedDict


class ExampleAvroAnotherExample(TypedDict, total=False):
    id: str
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_record.avsc'] = '''from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_records.avsc'] = '''from typing import Optional, TypedDict


class ExampleAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAddressUSRecord
    other_thing: ExampleOtherThing
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas nested_records_deep.avsc'] = '''from typing import Optional, TypedDict


class ExampleAvroAddressUSRecord(TypedDict, total=False):
    streetaddress: str
    city: str


class ExampleAvroNextOtherThing(TypedDict, total=False):
    thing1: str
    thing2: Optional[int]


class ExampleAvroOtherThing(TypedDict, total=False):
    thing1: str
    other_thing: ExampleAvroNextOtherThing


class ExampleAvroUser(TypedDict, total=False):
    name: str
    favorite_number: Optional[int]
    favorite_color: Optional[str]
    address: ExampleAvroAddressUSRecord
    other_thing: ExampleAvroOtherThing
'''

snapshots['SnapshotTypedDictFromSchemaString::test_snapshot_all_schemas no_optional_field_record.avsc'] = '''from typing import TypedDict


class ExampleAvroAnotherExample(TypedDict, total=False):
    id: str
'''
