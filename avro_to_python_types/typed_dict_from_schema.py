from .constants import OPTIONAL
from .generate_typed_dict import GenerateTypedDict
from .schema_mapping import prim_to_type, logical_to_python_type
from enum import Enum
from fastavro.schema import (
    load_schema,
    expand_schema,
    parse_schema,
    load_schema_ordered,
    fullname,
)
import ast
import astunparse
import black
import json

from avro_to_python_types.constants import (
    ENUM_CLASS,
    FIELDS,
    LOGICAL_TYPE,
    NAME,
    NULL,
    SYMBOLS,
    TYPE,
    ITEMS,
)


class AvroSubType(Enum):
    ENUM = "enum"
    RECORD = "record"
    ARRAY = "array"


def is_nullable(field):
    if isinstance(field[TYPE], list):
        for ftype in field[TYPE]:
            if ftype == NULL:
                return True
    return False


def field_type_is_of_type(field_type, type_name):
    """
    Check that the field type has a particular type, or a list with that type
    Compare the type of the dict representing this object's type against the
    provided type_name.  So this generic func can be used to detect many
    different types.
    """

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


def get_union_type(union_list: list):
    """Get the non null type from the union list"""
    for field in union_list:
        if isinstance(field, str) and field == NULL:
            continue
        return field


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
    """
    The fields processed by this module have already been parsed by fastavro.
    Fastavro alters the 'name' property of the enum type to be prefixed with
    the namespace of the schema.  This is what we're after here.
    """
    if isinstance(enum_type, list):
        for list_type in list(enum_type):
            if isinstance(list_type, dict) and NAME in list_type:
                return list_type[NAME]
    elif isinstance(enum_type, dict) and NAME in enum_type:
        return enum_type[NAME]
    else:
        raise Exception("invalid schema, enum type has no name")


def get_enum_symbols(enum_type):
    """
    Avro enums are strings and the entries are in the 'symbols' property of the
    enum type
    """
    if isinstance(enum_type, list):
        for list_type in list(enum_type):
            if isinstance(list_type, dict):
                return list_type[SYMBOLS]
    elif isinstance(enum_type, dict) and NAME in enum_type:
        return enum_type[SYMBOLS]
    else:
        raise Exception("invalid schema, enum type has no name")


def get_array_items(array_type):
    """
    Return the item type for the array.  Either a reference to a composite obj
    or a primative

    """
    if isinstance(array_type, list):
        for list_type in list(array_type):
            if isinstance(list_type, dict) and ITEMS in array_type:
                return list_type[ITEMS]
    elif isinstance(array_type, dict) and ITEMS in array_type:
        return array_type[ITEMS]
    else:
        raise Exception("invalid schema, array type has no items")


def get_logical_type(types):
    """
    Logical types can be dates, datetimes, UUIDs etc.
    """
    if not isinstance(types, list) and not isinstance(types, dict):
        raise ValueError("not a logical type: {}".format(types))
    elif isinstance(types, dict):
        return types[LOGICAL_TYPE]
    for ftype in types:
        if isinstance(ftype, dict):
            return ftype[LOGICAL_TYPE]
    raise ValueError(f"unexpected error in logical type: {types}")


def resolve_enum_str(enums: dict):
    return "\n\n".join(enums.values()) if len(enums) > 0 else ""


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
    This is the main function for the module.  It will parse a schema and return a
    concrete type which extends the TypedDict class.  It currently supports most
    primitive, logical, union and array types.  It does not support microsecond
    precision time types and durations.
    """
    body = []
    tree = ast.Module(body)
    body = tree.body

    def type_for_schema_record(record_schema, imports, enums, complex_types):
        type_name = "".join(
            word[0].upper() + word[1:] for word in record_schema["name"].split(".")
        )
        try:
            our_type = GenerateTypedDict(type_name)
            for field in record_schema[FIELDS]:
                name = field[NAME]
                if field_type_is_of_type(
                    field[TYPE], AvroSubType.RECORD.value
                ) and isinstance(field[TYPE], list):
                    """union with complex type - This section processes the type from a
                    union contining an expanded type, recursively.  Fastavro will expand
                    the types for the union the first time it encounters them and use a
                    reference thereafter.  So the first time it will be prcessed here and
                    subsequently in the primitives section.
                    """
                    union_field = get_union_type(field[TYPE])
                    nested = type_for_schema_record(
                        union_field, imports, enums, complex_types
                    )
                    body.append(nested.tree)
                    if is_nullable(field):
                        our_type.add_optional_element(name, nested.name)
                    else:
                        our_type.add_required_element(name, nested.name)
                    complex_types.append(nested.name)
                elif field_type_is_of_type(field[TYPE], AvroSubType.RECORD.value):
                    """nested - This processes an expanded nested type recursively."""
                    nested = type_for_schema_record(
                        field[TYPE], imports, enums, complex_types
                    )
                    body.append(nested.tree)
                    if is_nullable(field):
                        our_type.add_optional_element(name, nested.name)
                    else:
                        our_type.add_required_element(name, nested.name)
                    complex_types.append(nested.name)
                elif field_type_is_of_type(field[TYPE], LOGICAL_TYPE):
                    """logical - This section processes logical types.  This necessitates
                    importing packages like date, datetime, uuid and decimal hence the
                    imports collection"""
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
                elif field_type_is_of_type(field[TYPE], AvroSubType.ENUM.value):
                    """Enumerations are processed by adding an enum class to the
                    python file.  At the moment that means that the same enum used in
                    different schemas will result in that enum being duplicated, but
                    with a different name.  We can revisit that if necessary.
                    """
                    imports.append(
                        "from {} import {}\n".format(AvroSubType.ENUM.value, ENUM_CLASS)
                    )
                    """ The enum class name is composed the same way as the typedict
                        name is """
                    enum_class_name = "".join(
                        word[0].upper() + word[1:]
                        for word in get_enum_class(field[TYPE]).split(".")
                    )
                    enum_class = f"class {enum_class_name}(Enum):\n"
                    if not enum_class in enums.keys():
                        for e in get_enum_symbols(field[TYPE]):
                            enum_class += f"    {e} = '{e}'\n"
                        enum_class += "\n\n"
                        enums[enum_class] = enum_class
                    if is_nullable(field):
                        our_type.add_optional_element(name, enum_class_name)
                    else:
                        our_type.add_required_element(name, enum_class_name)
                    complex_types.append(enum_class_name)
                # array
                elif field_type_is_of_type(field[TYPE], AvroSubType.ARRAY.value):
                    """Array types are either primitive or complex.  Note that the
                    element added to the ast tree is a list of some type element"""
                    items_type = get_array_items(field[TYPE])
                    if field_type_is_of_type(items_type, AvroSubType.RECORD.value):
                        """Arrays is for a complex nested type"""
                        nested = type_for_schema_record(
                            items_type, imports, enums, complex_types
                        )
                        body.append(nested.tree)
                        if is_nullable(field):
                            our_type.add_optional_element(name, f"list({nested.name})")
                        else:
                            our_type.add_required_element(name, f"list({nested.name})")
                        complex_types.append(nested.name)
                    else:
                        """Array is of a prmitive type"""
                        if not items_type in prim_to_type.keys():
                            items_type_name = "".join(
                                word[0].upper() + word[1:]
                                for word in items_type.split(".")
                            )
                            array_type = (
                                items_type_name
                                if items_type_name in complex_types
                                else prim_to_type[items_type]
                            )
                        else:
                            array_type = prim_to_type[items_type]
                        if is_nullable(field):
                            our_type.add_optional_element(name, f"list({array_type})")
                        else:
                            our_type.add_required_element(name, f"list({array_type})")
                # primitive
                else:
                    """Ths section process a primitive type or a named complex type."""
                    if isinstance(field[TYPE], list):
                        for fld in field[TYPE]:
                            if fld != NULL:
                                field_type = fld
                    else:
                        field_type = get_type(field[TYPE])
                    if not field_type in prim_to_type.keys():
                        field_type_name = "".join(
                            word[0].upper() + word[1:] for word in field_type.split(".")
                        )
                        reference_type = (
                            field_type_name
                            if field_type_name in complex_types
                            else prim_to_type[field_type]
                        )
                    else:
                        reference_type = prim_to_type[field_type]
                    if is_nullable(field):
                        our_type.add_optional_element(name, reference_type)
                    else:
                        our_type.add_required_element(name, reference_type)
        except Exception as e:
            """If an error occurs while processing a field provide an error message
            containing the schema and field where the problem is so that they
            have a fighting chance to fix the prblem"""
            raise Exception(
                f"Failed to transform schema: [{fullname(schema)}] field: "
                + f"[{record_schema[NAME]}.{name}] for reason {e}"
            )
        return our_type

    imports = []
    enums = {}
    complex_types = []
    main_type = type_for_schema_record(schema, imports, enums, complex_types)

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


def typed_dict_from_schema_file(schema_path, referenced_schema_files=None):
    if referenced_schema_files:
        referenced_schema_files.append(schema_path)
        schema = load_schema_ordered(referenced_schema_files)
    else:
        schema = expand_schema(load_schema(schema_path))
    return types_for_schema(schema)
