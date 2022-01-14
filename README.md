# avro-to-python-types

A library for converting avro schemas to python types.

Currently, it supports converting `record`s to `TypedDict`. If you would like to see more features added, please open up an issue.

## Why would I want this?

This library is targeted to people writing code generation for python apps that are using [avro](https://avro.apache.org/docs/current/spec.html).

## Usage

This library does [one thing](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well), it converts Avro schemas to python types.

To get up and running quickly, you can use this to simply load schemas and print out the python
code that is generated.

```python
import glob
from avro_to_python_types import typed_dict_from_schema_file

schema_files = glob.glob("schemas/*.avsc")

for schema_file in schema_files:
    types = typed_dict_from_schema_file(schema_file)
    print(types) 

```

For a real world example of syncing a directory of schemas into a directory of matching python typed dictionaries
check out the example app [here](/examples/sync_types)

To try it out, simply clone this repo and run:

`poetry env use 3.9`
- This must be done as this library only supports Python 3.9 and above for type generation. You can still use this library in apps that use a lower Python version, as long as Python 3.9 is the active version when the types are generated (either locally or in your CI system).

`poetry install`

`poetry run sync-example`

For some more advanced examples, like referencing other schema files by their full name take a look at the tests [here](/tests)

### Referencing schemas

This library supports referencing schemas in different files by their fullname.

In order for this behaviour to work, all schemas must be in the same directory and use the following naming convention: `namespace.name.avsc`. Note that is the same as `fullname.avsc`

For more on this checkout the docs for fastavro [here](https://fastavro.readthedocs.io/en/latest/schema.html#fastavro._schema_py.load_schema).

An example of this can be found in the tests.

### Example output

The following example shows the type generated for a given schema.

```json
{
  "namespace": "example",
  "type": "record",
  "name": "User",
  "fields": [
    { "name": "name", "type": "string" },
    { "name": "favorite_number", "type": ["null", "int"] },
    { "name": "favorite_color", "type": ["null", "string"] },
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
          { "name": "thing2", "type": ["null", "int"] }
        ]
      }
    }
  ]
}
```

```python
from typing import TypedDict, Optional

# total=False allows us to skip passing optional fields into the constructor
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
    address: AddressUSRecord
    other_thing: OtherThing

```

## Testing

To run unit tests, run `poetry run pytest`.

You can also run tests in docker via `make test`

## Requirements

Python 3.9 or greater.
