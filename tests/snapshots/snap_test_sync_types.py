# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['SnapshotTestSyncedTypes::test_synced_types test_synced_types1'] = {
    'address': {
        'city': 'bergsville',
        'streetaddress': '154 Sparkling Heaven Dr'
    },
    'appt_date': GenericRepr('datetime.date(1993, 4, 21)'),
    'birthdate': GenericRepr('datetime.date(1989, 1, 11)'),
    'favorite_color': 'cyan',
    'favorite_number': 41,
    'name': 'walter',
    'time_of_day_birth': GenericRepr('datetime.time(12, 21, 45, 3000)'),
    'timestamp_of_birth': GenericRepr('datetime.datetime(1989, 1, 11, 1, 21, 45, tzinfo=datetime.timezone.utc)'),
    'uuid_of_birth_record': GenericRepr("UUID('e6a848a6-2682-4e9c-afe2-895f9bd45ff8')"),
    'weight': GenericRepr("Decimal('12.55')")
}

snapshots['SnapshotTestSyncedTypes::test_synced_types test_synced_types2'] = {
    'address': {
        'city': 'Dulock',
        'streetaddress': '1 Bowling Lawn Green'
    },
    'appt_date': GenericRepr('datetime.date(1993, 2, 21)'),
    'birthdate': GenericRepr('datetime.date(1999, 1, 11)'),
    'favorite_color': 'red',
    'favorite_number': 666,
    'name': 'george',
    'time_of_day_birth': GenericRepr('datetime.time(4, 21, 45, 5000)'),
    'timestamp_of_birth': GenericRepr('datetime.datetime(1999, 2, 11, 2, 22, 45, tzinfo=datetime.timezone.utc)'),
    'uuid_of_birth_record': GenericRepr("UUID('6c6a29f9-185e-476f-8055-ec91530ee561')"),
    'weight': GenericRepr("Decimal('44.55')")
}

snapshots['SnapshotTestSyncedTypes::test_synced_types test_synced_types3'] = {
    'address': {
        'city': 'Springfield',
        'streetaddress': '66 Springfield Cr'
    },
    'appt_date': GenericRepr('datetime.date(1944, 4, 21)'),
    'birthdate': GenericRepr('datetime.date(1911, 1, 11)'),
    'favorite_color': 'black',
    'favorite_number': 92,
    'name': 'marie',
    'time_of_day_birth': GenericRepr('datetime.time(1, 13, 37, 9000)'),
    'timestamp_of_birth': GenericRepr('datetime.datetime(1989, 1, 11, 3, 21, 45, tzinfo=datetime.timezone.utc)'),
    'uuid_of_birth_record': GenericRepr("UUID('6c6a29f9-185e-476f-8055-ec91530ee561')"),
    'weight': GenericRepr("Decimal('26.30')")
}
