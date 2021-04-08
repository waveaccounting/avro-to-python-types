from .constants import OPTIONAL
from .generate_typed_dict import GenerateTypedDict
from .schema_mapping import prim_to_type, logical_to_python_type
from fastavro.schema import load_schema, expand_schema, parse_schema
import ast
import astunparse
import black
import json

from avro_to_python_types.constants import (
    ENUM,
    ENUM_CLASS,
    FIELDS,
    LOGICAL_TYPE,
    NAME,
    NULL,
    RECORD,
    STRING,
    SYMBOLS,
    TYPE,
)


def is_nullable(field):
    if isinstance(field[TYPE], list):
        for ftype in field[TYPE]:
            if ftype == NULL:
                return True
    return False


def field_type_is_of_type(field_type, type_name):
    """Check that the field type has a particular type, or a list with that type"""

    def dict_type_is_of_type(dict_type, type_name):
        return (TYPE in dict_type and dict_type[TYPE] == type_name) or (
            type_name in dict_type
        )  # logicalType

    if isinstance(field_type, list):
        for type_from_list in list(field_type):
            if isinstance(type_from_list, dict):
                return dict_type_is_of_type(type_from_list, type_name)
    elif isinstance(field_type, dict):
        return dict_type_is_of_type(field_type, type_name)
    else:
        return False


def get_type(types):
    if not isinstance(types, list) and not isinstance(types, dict):
        return types
    elif isinstance(types, dict):
        return types[TYPE]
    for ftype in types:
        if ftype != NULL:
            return ftype
    raise ValueError("no valid type in list: {}".format(types))


def get_enum_class(enum_type):
    if isinstance(enum_type, list):
        for list_type in list(enum_type):
            if isinstance(list_type, dict) and NAME in list_type:
                return list_type[NAME]
    elif isinstance(enum_type, dict) and NAME in enum_type:
        return enum_type[NAME]
    else:
        raise Exception("invalid schema, enum type has no name")


def get_enum_symbols(enum_type):
    if isinstance(enum_type, list):
        for list_type in list(enum_type):
            if isinstance(list_type, dict):
                return list_type[SYMBOLS]
    elif isinstance(enum_type, dict) and NAME in enum_type:
        return enum_type[SYMBOLS]
    else:
        raise Exception("invalid schema, enum type has no name")


def get_logical_type(types):
    if not isinstance(types, list) and not isinstance(types, dict):
        raise ValueError("not a logical type: {}".format(types))
    elif isinstance(types, dict):
        return types[LOGICAL_TYPE]
    for ftype in types:
        if isinstance(ftype, dict):
            return ftype[LOGICAL_TYPE]
    raise ValueError(f"unexpected error in logical type: {types}")


def resolve_enum_str(enums: list):
    return "\n\n".join(enums) if len(enums) > 0 else ""


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

    def type_for_schema_record(record_schema, imports, enums):
        type_name = "".join(
            word[0].upper() + word[1:] for word in record_schema["name"].split(".")
        )
        our_type = GenerateTypedDict(type_name)
        for field in record_schema[FIELDS]:
            name = field[NAME]
            # nested
            if field_type_is_of_type(field[TYPE], RECORD):
                nested = type_for_schema_record(field[TYPE], imports, enums)
                body.append(nested.tree)
                if is_nullable(field):
                    our_type.add_optional_element(name, nested.name)
                else:
                    our_type.add_required_element(name, nested.name)
                continue
            # logical
            if field_type_is_of_type(field[TYPE], LOGICAL_TYPE):
                logical_type = logical_to_python_type[get_logical_type(field[TYPE])]
                imports.append(
                    "from {} import {}\n".format(
                        logical_type.split(".")[0], logical_type.split(".")[1]
                    )
                )
                if is_nullable(field):
                    our_type.add_optional_element(name, logical_type.split(".")[1])
                else:
                    our_type.add_required_element(name, logical_type.split(".")[1])
            # enum
            elif field_type_is_of_type(field[TYPE], ENUM):
                imports.append("from {} import {}\n".format(ENUM, ENUM_CLASS))
                enum_class_name = "".join(
                    word[0].upper() + word[1:]
                    for word in get_enum_class(field[TYPE]).split(".")
                )
                enum_class = f"class {enum_class_name}(Enum):\n"
                for e in get_enum_symbols(field[TYPE]):
                    enum_class += f"    {e} = {e}\n"
                enum_class += "\n\n"
                enums.append(enum_class)
                if is_nullable(field):
                    our_type.add_optional_element(name, enum_class_name)
                else:
                    our_type.add_required_element(name, enum_class_name)
            # primitive
            else:
                _type = get_type(field[TYPE])
                if is_nullable(field):
                    our_type.add_optional_element(name, prim_to_type[_type])
                else:
                    our_type.add_required_element(name, prim_to_type[_type])
        return our_type

    imports = []
    enums = []
    main_type = type_for_schema_record(schema, imports, enums)

    additional_types = []
    # import the Optional type only if required
    if OPTIONAL in ast.dump(main_type.tree):
        additional_types.append(OPTIONAL)
    additional_types.append("TypedDict")
    additional_types_as_str = ", ".join(additional_types)

    imports.append(f"from typing import {additional_types_as_str}\n")

    body.append(main_type.tree)
    imports = sorted(list(set(imports)))

    generated_code = (
        "".join(imports)
        + resolve_enum_str(enums)
        + astunparse.unparse(_dedupe_ast(tree))
    )
    formatted_code = black.format_str(generated_code, mode=black.FileMode())
    return formatted_code
    
def typed_dict_from_schema_string(schema_string):
    schema = parse_schema(json.loads(schema_string))
    return types_for_schema(schema)


def typed_dict_from_schema_file(schema_path):
    schema = expand_schema(load_schema(schema_path))
    return types_for_schema(schema)
