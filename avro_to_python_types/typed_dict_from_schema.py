from .generate_typed_dict import GenerateTypedDict
from .schema_mapping import prim_to_type
from fastavro.schema import load_schema, expand_schema, parse_schema
import ast
import json
import astor


def is_nullable(field):
    if isinstance(field["type"], list):
        if field["type"][0] == "null":
            return True
    return False


def is_nested(field):
    if isinstance(field["type"], dict):
        return True
    return False


def _dedupe_ast(tree):
    """Takes an AST that has multiple identical classes defined and dedupes them."""
    ###
    # As an intermediate step in the typegen process we fully expand the schema, this will
    # result in all referenced types being defined with their namespace - even if the same()
    # one is defines more than once. This is of course not valid, and we want to dedupe it.
    # https://fastavro.readthedocs.io/en/latest/schema.html#fastavro._schema_py.expand_schema
    ###

    all_types = tree.body
    existing_type_names = []
    deduped_types = []
    for current_type in all_types:
        type_name = current_type.body[0].name
        if type_name in existing_type_names:
            continue
        existing_type_names.append(type_name)
        deduped_types.append(current_type)

    tree.body = deduped_types
    return tree


def types_for_schema(schema):

    body = []
    tree = ast.Module(body)
    body = tree.body

    def type_for_schema_record(record_schema):
        type_name = record_schema["name"].replace(".", "_")
        our_type = GenerateTypedDict(type_name)
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
                type = field["type"][1]
                our_type.add_optional_element(name, prim_to_type[type])
            else:
                type = field["type"]
                our_type.add_required_element(name, prim_to_type[type])
        return our_type

    main_type = type_for_schema_record(schema)
    body.append(main_type.tree)

    imports = "from typing import TypedDict, Optional\n\n"
    types = astor.to_source(_dedupe_ast(tree))
    return imports + types


def typed_dict_from_schema_string(schema_string):
    schema = parse_schema(json.loads(schema_string))
    return types_for_schema(schema)


def typed_dict_from_schema_file(schema_path):
    schema = expand_schema(load_schema(schema_path))

    return types_for_schema(schema)
