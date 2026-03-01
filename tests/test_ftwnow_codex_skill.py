import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "ftwnow-codex"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
LINE_GATE_SCRIPT = SKILL_DIR / "scripts" / "effective_loc_gate.py"
HALT_REPORT_SCRIPT = SKILL_DIR / "scripts" / "emit_halt_report.py"


class FtwnowCodexSkillTests(unittest.TestCase):
    def test_required_files_exist(self):
        self.assertTrue(SKILL_MD.exists(), "SKILL.md is missing")
        self.assertTrue(OPENAI_YAML.exists(), "agents/openai.yaml is missing")

    def test_skill_markdown_length_gate(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertLessEqual(
            len(lines),
            400,
            f"SKILL.md has {len(lines)} lines (>400)",
        )

    def test_frontmatter_name_and_description(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"), "SKILL.md must start with frontmatter")
        self.assertIn("\nname: ftwnow-codex\n", content, "name must be ftwnow-codex")
        self.assertIn("\ndescription:", content, "description field is missing")

    def test_tool_mapping_uses_mcp_prefix(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        mapping_section = re.search(
            r"## Codex MCP Tool Mapping(.*?)(\n## |\Z)",
            content,
            flags=re.S,
        )
        self.assertIsNotNone(mapping_section, "Missing 'Codex MCP Tool Mapping' section")
        listed = re.findall(r"`(mcp__[a-z0-9_]+)`", mapping_section.group(1))
        self.assertGreaterEqual(len(listed), 8, "Not enough MCP tool mappings listed")
        for tool_name in listed:
            self.assertTrue(tool_name.startswith("mcp__"))

    def test_internal_markdown_refs_exist(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        refs = re.findall(r"`((?:agents|rules|checklists|references)/[^`]+)`", content)
        self.assertGreaterEqual(len(refs), 10, "Expected richer file references in SKILL.md")
        missing = [p for p in refs if not (SKILL_DIR / p).exists()]
        self.assertFalse(missing, f"Missing referenced files: {missing}")

    def test_scripts_exist(self):
        self.assertTrue(LINE_GATE_SCRIPT.exists(), "scripts/effective_loc_gate.py is missing")
        self.assertTrue(HALT_REPORT_SCRIPT.exists(), "scripts/emit_halt_report.py is missing")

    def test_line_gate_script_flags_oversized_file(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "oversized.ts"
            tmp.write_text("\n".join([f"const v{i} = {i}" for i in range(401)]), encoding="utf-8")
            proc = subprocess.run(
                ["python3", str(LINE_GATE_SCRIPT), str(tmp)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertIn("HALT", proc.stdout)


if __name__ == "__main__":
    unittest.main()
