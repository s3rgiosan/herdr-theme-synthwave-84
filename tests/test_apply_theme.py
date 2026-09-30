import importlib.machinery
import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
loader = importlib.machinery.SourceFileLoader("apply_theme", str(ROOT / "bin" / "apply-theme"))
spec = importlib.util.spec_from_loader("apply_theme", loader)
apply_theme = importlib.util.module_from_spec(spec)
loader.exec_module(apply_theme)

KEYS = '[keys]\nprefix = "ctrl+b"\n'
UI = '[ui]\nstatus_indicators = "symbols"\n'
OLD_THEME = (
    '[theme]\nname = "nord"\n\n'
    '[theme.custom]\naccent = "#123456"\n\n'
    '[theme.custom.dark]\npanel_bg = "#000000"\n\n'
)


class SplitTests(unittest.TestCase):
    def test_no_theme_table(self):
        rest, theme, insert_at = apply_theme.split_theme_tables(KEYS + "\n" + UI)
        self.assertEqual(rest, KEYS + "\n" + UI)
        self.assertEqual(theme, "")
        self.assertIsNone(insert_at)

    def test_theme_tables_between_other_tables(self):
        config = KEYS + "\n" + OLD_THEME + UI
        rest, theme, insert_at = apply_theme.split_theme_tables(config)
        self.assertEqual(rest, KEYS + "\n" + UI)
        self.assertEqual(theme, OLD_THEME)
        self.assertEqual(insert_at, len(KEYS) + 1)

    def test_array_table_ends_theme_table(self):
        config = '[theme]\nname = "nord"\n\n[[keys.command]]\nkey = "prefix+x"\n'
        rest, theme, _ = apply_theme.split_theme_tables(config)
        self.assertEqual(theme, '[theme]\nname = "nord"\n\n')
        self.assertEqual(rest, '[[keys.command]]\nkey = "prefix+x"\n')

    def test_similar_table_name_is_not_theme(self):
        config = '[themes]\nx = 1\n'
        _, theme, insert_at = apply_theme.split_theme_tables(config)
        self.assertEqual(theme, "")
        self.assertIsNone(insert_at)


class ReplaceTests(unittest.TestCase):
    def test_block_appended_when_no_theme(self):
        block = apply_theme.theme_block()
        result = apply_theme.replace_theme_tables(KEYS, block)
        self.assertEqual(result, KEYS + "\n" + block)

    def test_block_replaces_theme_in_place(self):
        block = apply_theme.theme_block()
        result = apply_theme.replace_theme_tables(KEYS + "\n" + OLD_THEME + UI, block)
        self.assertTrue(result.startswith(KEYS + "\n[theme]\n"))
        self.assertTrue(result.endswith("\n\n" + UI))
        self.assertNotIn('"nord"', result)

    def test_apply_is_idempotent(self):
        block = apply_theme.theme_block()
        once = apply_theme.replace_theme_tables(KEYS + "\n" + OLD_THEME + UI, block)
        twice = apply_theme.replace_theme_tables(once, block)
        self.assertEqual(once, twice)

    def test_block_sets_every_token(self):
        tokens = {
            "accent", "panel_bg", "sidebar_bg", "active_row_bg", "selection_bg",
            "surface0", "surface1", "surface_dim", "overlay0", "overlay1", "text",
            "subtext0", "mauve", "green", "yellow", "red", "blue", "teal", "peach",
        }
        block = apply_theme.theme_block()
        keys = {line.split("=")[0].strip() for line in block.splitlines() if "=" in line}
        self.assertTrue(tokens <= keys)


class ApplyRestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.config = self.tmp / "config.toml"
        env = {
            "HERDR_CONFIG_PATH": str(self.config),
            "HERDR_PLUGIN_STATE_DIR": str(self.tmp / "state"),
            "HERDR_BIN_PATH": shutil.which("true"),
        }
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(shutil.rmtree, self.tmp)

    def round_trip(self, original):
        self.config.write_text(original)
        apply_theme.apply(self.config)
        self.assertIn('accent = "#ff7edb"', self.config.read_text())
        apply_theme.restore(self.config)
        self.assertEqual(self.config.read_text(), original)

    def test_restore_reproduces_config_with_theme(self):
        self.round_trip(KEYS + "\n" + OLD_THEME + UI)

    def test_restore_reproduces_config_with_theme_at_end(self):
        self.round_trip(KEYS + "\n" + OLD_THEME)

    def test_restore_reproduces_config_without_theme(self):
        self.round_trip(KEYS + "\n" + UI)

    def test_second_apply_keeps_first_backup(self):
        original = KEYS + "\n" + OLD_THEME + UI
        self.config.write_text(original)
        apply_theme.apply(self.config)
        apply_theme.apply(self.config)
        apply_theme.restore(self.config)
        self.assertEqual(self.config.read_text(), original)

    def test_failed_check_rolls_back(self):
        original = KEYS
        self.config.write_text(original)
        with mock.patch.dict(os.environ, {"HERDR_BIN_PATH": shutil.which("false")}):
            with self.assertRaises(SystemExit):
                apply_theme.apply(self.config)
        self.assertEqual(self.config.read_text(), original)
        self.assertFalse((self.tmp / "state" / apply_theme.BACKUP_NAME).exists())

    def test_managed_theme_is_not_backed_up(self):
        self.config.write_text(KEYS)
        apply_theme.apply(self.config)
        (self.tmp / "state" / apply_theme.BACKUP_NAME).unlink()
        apply_theme.apply(self.config)
        self.assertFalse((self.tmp / "state" / apply_theme.BACKUP_NAME).exists())

    def test_block_carries_managed_marker_and_base(self):
        block = apply_theme.theme_block()
        self.assertIn(apply_theme.MANAGED_BY, block)
        self.assertIn('name = "dracula"', block)

    def test_restore_without_backup_fails(self):
        self.config.write_text(KEYS)
        with self.assertRaises(SystemExit):
            apply_theme.restore(self.config)


if __name__ == "__main__":
    unittest.main()
