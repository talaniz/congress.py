# Changelog

All notable user-facing changes to this project will be documented in this
file. This changelog follows the [Keep a Changelog](https://keepachangelog.com/)
style and uses the package version from `pyproject.toml`.

## [Unreleased]

### Added

- MkDocs documentation site using MkDocs Material.
- Documentation pages for installation, quickstart, CLI usage, SDK usage, API
  reference, contributing, and changelog.
- mkdocstrings-generated API reference for `client.py`, `models.py`, and
  `exceptions.py`.
- `CongressClient.list_recent_bills(limit=10)` convenience method for safe
  recent bill discovery.

### Changed

- Shortened the README into a front door for the project and documentation
  site.

## [0.1.0] - 2026-06-05

### Added

- Initial `congress_py` SDK package using a `src` layout.
- `CongressClient` with Congress session and bill endpoints.
- Typed models for bills, bill actions, and bill summaries.
- Typer-based `congress` CLI.
- CLI credential resolution using `--api-key`, `CONGRESS_API_KEY`, and
  `~/.congress/config.toml`.
- Bill workflow commands for details, actions, and summaries.
- Bill listing pagination and multi-page iteration.
- Mocked SDK and CLI tests.

### Changed

- Refactored the project into the `congress_py` package.
- Updated README examples as SDK and CLI behavior expanded.

### Fixed

- Supported the `/congress/current` item response shape.
- Made bill URL optional for single-bill API responses.
- Fixed CLI JSON serialization for dataclass and namedtuple outputs.
