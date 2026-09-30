# herdr-theme-synthwave-84

A [Herdr](https://herdr.dev) plugin that applies the **Synthwave '84** neon palette
to Herdr's UI: sidebar, panels, selection, accents, and status colors.

Synthwave '84 was created by [Robb Owen](https://github.com/robb0wen/synthwave-vscode).
This plugin adapts its colors for Herdr and is not affiliated with Herdr.

## Install

Requires Herdr 0.9.0+, macOS or Linux, and Python 3.

```sh
herdr plugin install s3rgiosan/herdr-theme-synthwave-84
herdr plugin action invoke apply --plugin herdr-theme-synthwave-84
```

`apply` replaces the `[theme]` and `[theme.*]` tables in Herdr's `config.toml`
and keeps every other setting. Before the first apply it saves your previous
theme tables in the plugin state directory. The new config is checked with
`herdr config check`; an invalid result is rolled back. A running server is
reloaded, so the theme shows up without a restart.

Herdr reads `HERDR_CONFIG_PATH`, then `$XDG_CONFIG_HOME/herdr/config.toml`,
then `~/.config/herdr/config.toml`. The plugin edits the same file.

## Restore your previous theme

```sh
herdr plugin action invoke restore --plugin herdr-theme-synthwave-84
```

## Keybinding

The plugin ships without a keybinding. To add one, put this in `config.toml`:

```toml
[[keys.command]]
key = "prefix+shift+s"
type = "plugin_action"
command = "herdr-theme-synthwave-84.apply"
description = "apply Synthwave '84 theme"
```

## Manual install

[`themes/synthwave-84.toml`](themes/synthwave-84.toml) is a complete `[theme]`
block. Replace the `[theme]` table and all `[theme.custom]` subtables in your
`config.toml` with its contents, then run:

```sh
herdr config check
herdr server reload-config
```

The palette sets `auto_switch = false` and no `name`, because Herdr only accepts
built-in names there. All 19 color tokens are set, so the base theme never shows.

## Scope

The theme colors Herdr's own interface. Programs running inside panes keep the
colors of your terminal; pair it with a Synthwave '84 terminal theme for the
full look.

## Development

```sh
herdr plugin link "$PWD"
python3 -m unittest discover tests
```

## License

MIT. See [LICENSE](LICENSE).
