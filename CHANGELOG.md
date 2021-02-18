# Changelog
## 0.2.1

### Fixed

- An issue with parsing nullable fields
## 0.2.0

### Added

- `typed_dict_from_schema_file(schema_path)`

### Breaking Changes

- `schema_to_typed_dict` is now `typed_dict_from_schema_string`
- Types are now prepended by their namespace
