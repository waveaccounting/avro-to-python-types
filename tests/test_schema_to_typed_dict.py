import glob
from avro_to_python import schema_to_typed_dict
import snapshottest

test_json_files = glob.glob("tests/test_cases/*.avsc")


class SnapshotSchemaToTypedDict(snapshottest.TestCase):
    def test_snapshot_all_schemas(self):
        for test_json_file in test_json_files:
            with open(test_json_file) as f:
                avro_schema = f.read()
            test_output = schema_to_typed_dict(avro_schema)
            schema_name = test_json_file.rsplit("/", 1)[-1]
            self.assertMatchSnapshot(test_output, schema_name)
