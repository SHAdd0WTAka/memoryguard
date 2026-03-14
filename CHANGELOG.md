# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2026-03-14

### Fixed
- Fixed `NameError: name 'Table' is not defined` in dashboard.py - added missing `from rich.table import Table` import
- Fixed missing Rich UI component imports (`Table`, `Panel`, `Layout`, `Text`, etc.)

### Added
- Added dashboard screenshot to documentation
- Added this CHANGELOG.md

## [1.0.1] - 2025-03-05

### Fixed
- Fixed PyPI deployment configuration
- Updated GitHub Actions workflows

## [1.0.0] - 2025-03-05

### Added
- Initial release
- Core memory monitoring functionality
- Valgrind integration for C extensions
- Live terminal dashboard (requires rich)
- Decorator-based memory tracking
- Tool profiling and orchestration
- CI/CD integration support
