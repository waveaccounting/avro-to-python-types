# avro-to-python-types

A library for converting avro schemas to python types.

Currently, it supports converting `record`s to `TypedDict`. If you would like to see more features added, please open up an issue.

## Why would I want this?

This library is target to people writing code generation for python apps that are using avro.

## Example usage

```python
from avro_to_python_types import schema_to_typed_dict

with open(test_json_file) as f:
    avro_schema = f.read()
    output = schema_to_typed_dict(avro_schema)
    print(output)
```

The avro schema will produce the following python

```json
{
  "namespace": "example.avro",
  "type": "record",
  "name": "User",
  "fields": [
    { "name": "name", "type": "string" },
    { "name": "favorite_number", "type": ["int", "null"] },
    { "name": "favorite_color", "type": ["string", "null"] },
    {
      "name": "address",
      "type": {
        "type": "record",
        "name": "AddressUSRecord",
        "fields": [
          { "name": "streetaddress", "type": "string" },
          { "name": "city", "type": "string" }
        ]
      }
    },
    {
      "name": "other_thing",
      "type": {
        "type": "record",
        "name": "OtherThing",
        "fields": [
          { "name": "thing1", "type": "string" },
          { "name": "thing2", "type": ["int", "null"] }
        ]
      }
    }
  ]
}
```

```python
from typing import TypedDict, Optional

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
```
