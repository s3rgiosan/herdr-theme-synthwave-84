# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Synthwave '84 palette for Herdr's UI, covering all 19 customizable color tokens.
- `apply` action: writes the palette into `config.toml`, validates it with `herdr config check`, and reloads the server.
- `restore` action: puts back the `[theme]` tables saved before the first apply.
- `prefix+shift+s` keybinding for the `apply` action.
- Dracula base theme, a managed-by marker that keeps re-applies out of the backup, and a transparent panel background.
