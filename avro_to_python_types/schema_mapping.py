from enum import Enum


prim_to_type = {
    "null": "None",
    "boolean": "bool",
    "int": "int",
    "long": "int",
    "float": "float",
    "double": "float",
    "bytes": "bytes",
    "string": "str",
}


logical_to_python_type = {
    "date": "datetime.date",
    "time-millis": "datetime.time",
    "timestamp-millis": "datetime.datetime",
    "uuid": "uuid.UUID",
    "decimal": "decimal.Decimal",
}
