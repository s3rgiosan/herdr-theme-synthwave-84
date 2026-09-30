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
theme tables in the plugin state directory. The written block carries a
`# Managed by Herdr plugin: herdr-theme-synthwave-84` comment, so re-applying
never backs up the plugin's own theme. The new config is checked with
`herdr config check`; an invalid result is rolled back. A running server is
reloaded, so the theme shows up without a restart.

Herdr reads `HERDR_CONFIG_PATH`, then `$XDG_CONFIG_HOME/herdr/config.toml`,
then `~/.config/herdr/config.toml`. The plugin edits the same file.

Inside Herdr, `prefix+shift+s` runs the same action.

## Restore your previous theme

```sh
herdr plugin action invoke restore --plugin herdr-theme-synthwave-84
```

## Settings menu

Herdr's Settings → Theme menu lists built-in themes only, so Synthwave '84 does
not appear there. The palette sits on top of the built-in Dracula theme, which
is the entry the menu highlights. Every color is overridden, so choosing another
theme in the menu shows no change; run `restore` first to switch away.

## Manual install

[`themes/synthwave-84.toml`](themes/synthwave-84.toml) is a complete `[theme]`
block. Replace the `[theme]` table and all `[theme.custom]` subtables in your
`config.toml` with its contents, then run:

```sh
herdr config check
herdr server reload-config
```

The palette uses `dracula` as its base name, because Herdr only accepts built-in
names there, and sets `auto_switch = false`. All 19 color tokens are set, so the
base theme never shows. `panel_bg = "reset"` lets your terminal background show
through the panels.

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
