from .generate_typed_dict import GenerateTypedDict
import json

schema = json.loads(
    """
{"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}
"""
)


def is_nullable(field):
    if isinstance(field["type"], list):
        if field["type"][1] == "null":
            return True
    return False


def typed_dict():
    custom = GenerateTypedDict(schema["name"])
    for field in schema["fields"]:
        name = field["name"]
        if is_nullable(field):
            type = field["type"][0]
            custom.add_optional_element(name, type)
        else:
            type = field["type"]
            custom.add_required_element(name, type)
    print(custom.get_code())
