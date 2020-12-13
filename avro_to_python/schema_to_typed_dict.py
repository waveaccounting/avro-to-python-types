from .generate_typed_dict import GenerateTypedDict
from .schema_mapping import prim_to_type
import ast
import json
import astor


def is_nullable(field):
    if isinstance(field["type"], list):
        if field["type"][1] == "null":
            return True
    return False


def is_nested(field):
    if isinstance(field["type"], dict):
        return True
    return False


def type_for_schema(schema):
    body = []
    tree = ast.Module(body)
    body = tree.body

    def type_for_schema_record(record_schema):
        our_type = GenerateTypedDict(record_schema["name"])
        for field in record_schema["fields"]:
            name = field["name"]
            if is_nested(field):
                nested = type_for_schema_record(field["type"])
                body.append(nested.tree)
                if is_nullable(field):
                    our_type.add_optional_element(name, nested.name)
                else:
                    our_type.add_required_element(name, nested.name)
                continue
            if is_nullable(field):
                type = field["type"][0]
                our_type.add_optional_element(name, prim_to_type[type])
            else:
                type = field["type"]
                our_type.add_required_element(name, prim_to_type[type])
        return our_type

    main_type = type_for_schema_record(schema)
    body.append(main_type.tree)
    return tree


def schema_to_typed_dict(test_schema):
    new_type = type_for_schema(json.loads(test_schema))
    imports = "from typing import TypedDict, Optional\n\n"
    types = astor.to_source(new_type)
    return imports + types
