# Changelog
  
## 0.12.0
### Added
- Support for the "map" and "fixed" avro types.
### Changed
- Alphabetically sort generated imports.
- Gather imports from the same module onto a single line.
### Fixed
- An issue retrieving items from array types within lists of types.

## 0.11.2
### Changed
- Upgraded internal dependencies

## 0.11.1
### Changed
- Moved black from prod to dev dependencies and update lock file.

## 0.11.0
### Removed
- `astunparse` has been removed as the built-in `ast` module supports unparsing ASTs, as of Python 3.9.
### Changed
- Refactoring of AST deduplication logic.
  
## 0.10.0
### Changed
- Added the ability to provide schema references by their file names.  Useful when the
- schema types don't match the file names and fastavro can't automatically load them.
  
## 0.9.0
### Changed
- Added array type support

## 0.8.0
### Changed
- Added enum type support

## 0.7.0
### Added
- Optional arguments can now be skipped being passed into the TypedDict class constructor.
- Generated code is automatically formatted with `black`.

### Changed
- The `astor` library has been replaced with `astunparse`.

## 0.6.0
### Changed
- Make library compatible with Python 3.8

## 0.5.0
### Changed
- The `Optional` type is imported only if necessary.
- If both `Optional` and `TypedDict` are imported, the imports are sorted alphabetically.

## 0.4.0

### Added

- Support for logical types date, time-millis, timestamp-millis, UUID and decimal in the schema.
- Test cases for new types and modified the sample-types code to use the new types as well.

## 0.3.0

### Breaking Changes

- Generated classes now follow proper PEP 8 naming convention: https://www.python.org/dev/peps/pep-0008/#class-names
## 0.2.2

### Added

- `py.typed file`
## 0.2.1

### Fixed

- An issue with parsing nullable fields
## 0.2.0

### Added

- `typed_dict_from_schema_file(schema_path)`

### Breaking Changes

- `schema_to_typed_dict` is now `typed_dict_from_schema_string`
- Types are now prepended by their namespace
