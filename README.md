# avro-to-python-types

A library for converting avro schemas to python types.

Currently, it supports converting `record`s to `TypedDict`. If you would like to see more features added, please open up an issue.

## Why would I want this?

This library is target to people writing code generation for python apps that are using avro.

## Example usage

If you are using Avro (with our without Schema Registry) you will want to to have some type safety when you messages are deserialized.

(This example project)[/examples/sync_types] shows how to keep a directory of Avro schemas in sync with a directory of python files exposing their types.

To try it out, simply clone this repo and run

`poetry install`
`poetry run sync-example`

For example, this avro schema will produce the following python

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
