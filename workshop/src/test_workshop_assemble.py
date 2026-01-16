import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class TestWorkshopAssemble(unittest.TestCase):
    def test_slice_and_whole_file_sources(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)

            src = base / "src.md"
            src.write_text(
                "\n".join(
                    [
                        "before",
                        "<!-- slice:one -->",
                        "SLICED",
                        "<!-- /slice -->",
                        "after",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/Demo/AGENTS.md"}],
                    "sources": [
                        {"slice": "one", "slice-file": "src.md"},
                        {"file": "src.md"},
                    ],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS.md")

            output_path = artifacts[0].abspath
            self.assertTrue(output_path.exists())
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("SLICED", text)
            self.assertIn("before", text)

    def test_agent_filename_disambiguation_when_requested(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            (base / "a.md").write_text("A\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=1,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "_total_sections": 2,
                    "_agent_disambiguator": "section2",
                    "target_locations": [{"path": "~/Demo/AGENTS.md"}],
                    "sources": [{"file": "a.md"}],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS-section2.md")

    def test_agent_directory_target_defaults_to_agents_md(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            (base / "a.md").write_text("A\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.codex/"}],  # directory form
                    "sources": [{"file": "a.md"}],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS.md")

    def test_agent_directory_target_defaults_to_claude_md(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            (base / "a.md").write_text("A\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.claude/"}],  # directory form
                    "sources": [{"file": "a.md"}],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/CLAUDE.md")

    def test_sync_resolves_agent_directory_targets(self) -> None:
        import workshop.src.sync as sync
        from pathlib import Path

        sections = [
            sync.RecipeSection(
                recipe_file=Path("recipe.md"),
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.codex/"}],
                },
            ),
            sync.RecipeSection(
                recipe_file=Path("recipe.md"),
                index=1,
                config={
                    "name": "Demo2",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.claude/"}],
                },
            ),
        ]

        items = sync.build_sync_items_from_sections(sections)
        expected_codex = str(Path.home() / ".codex" / "AGENTS.md").replace("\\", "/").lower()
        expected_claude = str(Path.home() / ".claude" / "CLAUDE.md").replace("\\", "/").lower()
        self.assertEqual(items[0].targets[0].replace("\\", "/").lower(), expected_codex)
        self.assertEqual(items[1].targets[0].replace("\\", "/").lower(), expected_claude)

    def test_command_outputs_hook_and_markdown(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)

            (base / "prompts").mkdir(parents=True, exist_ok=True)
            (base / "prompts" / "murder.md").write_text("# Murder\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "murder",
                    "output_format": "command",
                    "target_locations": [
                        {"path": "~/.kiro/hooks/murder.kiro.hook"},
                        {"path": "~/.claude/commands/murder.md"},
                        {"path": "~/.codex/prompts/murder.md"},
                    ],
                    "sources": {
                        "kiro_hook": [{"file": "prompts/murder.md"}],
                        "command_md": [{"file": "prompts/murder.md"}],
                    },
                    "kiro_hook_config": {
                        "enabled": True,
                        "name": "Murder Cogitator",
                        "description": "Test",
                        "version": "1",
                        "when": {"type": "userTriggered"},
                        "then": {"type": "askAgent"},
                        "shortName": "murder",
                    },
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 2)

            rels = sorted([a.relpath for a in artifacts])
            self.assertEqual(rels[0], "command/murder/murder.kiro.hook")
            self.assertEqual(rels[1], "command/murder/murder.md")

            hook_art = [a for a in artifacts if a.relpath.endswith(".kiro.hook")][0]
            md_art = [a for a in artifacts if a.relpath.endswith(".md")][0]

            self.assertEqual(len(hook_art.targets), 1)
            self.assertEqual(len(md_art.targets), 2)

            import json

            hook_obj = json.loads(hook_art.abspath.read_text(encoding="utf-8"))
            self.assertEqual(hook_obj["then"]["type"], "askAgent")
            self.assertIn("# Murder", hook_obj["then"]["prompt"])

    def test_command_inline_sources(self) -> None:
        import workshop.src.assemble as assemble
        import json

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "doc-consistency-check",
                    "output_format": "command",
                    "target_locations": [
                        {"path": "~/.kiro/hooks/doc-consistency-check.kiro.hook"},
                        {"path": "~/.claude/commands/doc-consistency-check.md"},
                    ],
                    "sources": {
                        "kiro_hook": [{"inline": "INLINE HOOK PROMPT"}],
                        "command_md": [{"inline": "# Title\n\nINLINE MD"}],
                    },
                    "kiro_hook_config": {
                        "enabled": True,
                        "name": "Documentation Consistency Checker",
                        "description": "Test",
                        "version": "1",
                        "when": {"type": "userTriggered"},
                        "then": {"type": "askAgent"},
                        "shortName": "doc-consistency-check",
                    },
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 2)
            hook_art = [a for a in artifacts if a.relpath.endswith(".kiro.hook")][0]
            hook_obj = json.loads(hook_art.abspath.read_text(encoding="utf-8"))
            self.assertIn("INLINE HOOK PROMPT", hook_obj["then"]["prompt"])


if __name__ == "__main__":
    unittest.main()
