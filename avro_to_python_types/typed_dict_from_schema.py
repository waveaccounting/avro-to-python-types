from .constants import OPTIONAL
from .generate_typed_dict import GenerateTypedDict
from .schema_mapping import prim_to_type, logical_to_python_type
from fastavro.schema import load_schema, expand_schema, parse_schema
import ast
import json
import astor


def is_nullable(field):
    if isinstance(field["type"], list):
        for ftype in field["type"]:
            if ftype == "null":
                return True
    return False


def is_nested(field):
    if isinstance(field["type"], dict) and not is_logical_type(field["type"]):
        return True
    return False


def is_logical_type(field_type):
    if isinstance(field_type, list):
        for ftype in field_type:
            if ftype != "null" and isinstance(ftype, dict):
                return "logicalType" in ftype
    elif isinstance(field_type, dict):
        return "logicalType" in field_type
    return False


def get_type(types):
    if not isinstance(types, list) and not isinstance(types, dict):
        return types
    elif isinstance(types, dict):
        return types["type"]
    for ftype in types:
        if ftype != "null":
            return ftype
    raise ValueError("no valid type in list: {}".format(types))


def get_logical_type(types):
    if not isinstance(types, list) and not isinstance(types, dict):
        raise ValueError("not a logical type: {}".format(types))
    elif isinstance(types, dict):
        return types["logicalType"]
    for ftype in types:
        if isinstance(ftype, dict):
            return ftype["logicalType"]
    raise ValueError("unexpected error in logical type: {}".format(types))


def is_logical(field):
    return (
        isinstance(field["type"], dict) or isinstance(field["type"], list)
    ) and is_logical_type(field["type"])


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
    """
    This is the main function for the module.  It will parse a schema and return a concrete type
    which extends the TypedDict class.  It currently supports all primitive types as well as
    logical types except for the microsecond precision time types.
    """
    body = []
    tree = ast.Module(body)
    body = tree.body

    def type_for_schema_record(record_schema, imports):
        type_name = "".join(
            word[0].upper() + word[1:] for word in record_schema["name"].split(".")
        )
        our_type = GenerateTypedDict(type_name)
        for field in record_schema["fields"]:
            name = field["name"]
            if is_nested(field):
                nested = type_for_schema_record(field["type"], imports)
                body.append(nested.tree)
                if is_nullable(field):
                    our_type.add_optional_element(name, nested.name)
                else:
                    our_type.add_required_element(name, nested.name)
                continue
            if is_logical(field):
                logical_type = logical_to_python_type[get_logical_type(field["type"])]
                imports.append(
                    "from {} import {}\n".format(
                        logical_type.split(".")[0], logical_type.split(".")[1]
                    )
                )
                if is_nullable(field):
                    our_type.add_optional_element(name, logical_type.split(".")[1])
                else:
                    our_type.add_required_element(name, logical_type.split(".")[1])
            else:
                type = get_type(field["type"])
                if is_nullable(field):
                    our_type.add_optional_element(name, prim_to_type[type])
                else:
                    our_type.add_required_element(name, prim_to_type[type])
        return our_type

    imports = []
    main_type = type_for_schema_record(schema, imports)

    additional_types = []
    # import the Optional type only if required
    if OPTIONAL in ast.dump(main_type.tree):
        additional_types.append(OPTIONAL)
    additional_types.append("TypedDict")
    additional_types_as_str = ", ".join(additional_types)

    imports.append(f"from typing import {additional_types_as_str}\n")

    body.append(main_type.tree)
    imports = sorted(list(set(imports)))
    return "".join(imports) + "\n\n" + astor.to_source(_dedupe_ast(tree))


def typed_dict_from_schema_string(schema_string):
    schema = parse_schema(json.loads(schema_string))
    return types_for_schema(schema)


def typed_dict_from_schema_file(schema_path):
    schema = expand_schema(load_schema(schema_path))
    return types_for_schema(schema)
