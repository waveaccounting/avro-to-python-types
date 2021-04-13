import glob
from avro_to_python_types import (
    typed_dict_from_schema_string,
    typed_dict_from_schema_file,
)
import snapshottest

test_schema_files = glob.glob("tests/test_cases/*.avsc")
expandable_schema_files = glob.glob("tests/test_cases_expandable/*.avsc")
shopping_cart_files = glob.glob("tests/test_shopping_cart/*.avsc")


class SnapshotTypedDictFromOrder(snapshottest.TestCase):
    def test_snapshot_self_contained_schemas(self):
        for test_schema_file in test_schema_files:
            test_output = typed_dict_from_schema_file(test_schema_file)
            schema_name = test_schema_file.rsplit("/", 1)[-1]
            self.assertMatchSnapshot(test_output, schema_name)

    def test_snapshot_expandable_schemas(self):
        for test_schema_file in expandable_schema_files:
            test_output = typed_dict_from_schema_file(test_schema_file)
            schema_name = test_schema_file.rsplit("/", 1)[-1]
            self.assertMatchSnapshot(test_output, schema_name)


class SnapshotTypedDictArrayFromSchemaFile(snapshottest.TestCase):
    def test_array_map_schemas(self):
        for test_schema_file in shopping_cart_files:
            test_output = typed_dict_from_schema_file(test_schema_file)
            schema_name = test_schema_file.rsplit("/", 1)[-1]
            self.assertMatchSnapshot(test_output, schema_name)


class SnapshotTypedDictFromSchemaString(snapshottest.TestCase):
    def test_snapshot_all_schemas(self):
        for test_json_file in test_schema_files:
            with open(test_json_file) as f:
                avro_schema = f.read()
            test_output = typed_dict_from_schema_string(avro_schema)
            schema_name = test_json_file.rsplit("/", 1)[-1]
            self.assertMatchSnapshot(test_output, schema_name)
