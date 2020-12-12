from .generate_typed_dict import GenerateTypedDict
from .schema_mapping import prim_to_type
import json

test_schema = json.loads(
    """
{"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]},
     {"name": "address",
        "type": {
            "type" : "record",
            "name" : "AddressUSRecord",
            "fields" : [
                {"name": "streetaddress", "type": "string"},
                {"name": "city", "type": "string"}
            ]
        }
    }
 ]
}
"""
)


def is_nullable(field):
    if isinstance(field["type"], list):
        if field["type"][1] == "null":
            return True
    return False


def is_nested(field):
    if isinstance(field["type"], dict):
        return True
    return False


def type_for_record(schema):
    our_type = GenerateTypedDict(schema["name"])
    for field in schema["fields"]:
        if is_nested(field):
            continue
        name = field["name"]
        if is_nullable(field):
            type = field["type"][0]
            print(prim_to_type[type])
            our_type.add_optional_element(name, prim_to_type[type])
        else:
            type = field["type"]
            our_type.add_required_element(name, prim_to_type[type])
    return our_type


def typed_dict():
    new_type = type_for_record(test_schema)
    print(new_type.get_code())
