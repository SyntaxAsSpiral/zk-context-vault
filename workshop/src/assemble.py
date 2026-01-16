#!/usr/bin/env python3
"""
Context Assembly Script

Processes Obsidian recipe files with embedded YAML to assemble context content.
Supports:
- slice extraction via `slice` + `slice-file`
- whole-file inclusion via `file` only
- multi-section recipes via YAML document separators (`---`) inside the YAML block
- structured output formats: `agent`, `skill`, `power`

Outputs assembled artifacts to `.context/workshop/staging/` and updates
`.context/workshop/recipe-manifest.md` with run logs.

Usage: python assemble.py [--dry-run] [--verbose]
"""

import re
import yaml
import frontmatter
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import sys
import json
from typing import Any, Dict, Iterable, List, Optional, Tuple


def find_recipe_files(workshop_dir: Path) -> List[Path]:
    """Find all recipe .md files in workshop directory."""
    recipe_files = []
    for md_file in workshop_dir.glob("recipe-*.md"):
        if md_file.name != "recipe-manifest.md":
            recipe_files.append(md_file)
    return recipe_files


@dataclass(frozen=True)
class RecipeSection:
    recipe_file: Path
    index: int
    config: Dict[str, Any]


@dataclass(frozen=True)
class OutputArtifact:
    # Relative to staging_dir using posix separators (for stable IDs/logging)
    relpath: str
    abspath: Path
    targets: List[str]
    is_dir: bool


def _configure_stdio_utf8() -> None:
    # Windows terminals often default to cp1252; our logs include unicode glyphs.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _expand_target_path(p: str) -> str:
    # Preserve trailing separators (directory targets) by expanding via string ops.
    if p.startswith("~/"):
        return str(Path.home()) + "/" + p[2:]
    if p.startswith("~\\"):
        return str(Path.home()) + "\\" + p[2:]
    return p


def _norm_path_str(p: str) -> str:
    return p.replace("\\", "/").lower()


def _is_claude_target(p: str) -> bool:
    np = _norm_path_str(p)
    return "/.claude/" in np or np.endswith("/.claude")


def _is_dir_target_string(p: str) -> bool:
    return p.endswith("/") or p.endswith("\\")


def _default_agent_filename_for_target(target_path: str) -> str:
    # Claude consumes CLAUDE.md; everyone else consumes AGENTS.md.
    return "CLAUDE.md" if _is_claude_target(target_path) else "AGENTS.md"


def _is_kiro_hook_target(p: str) -> bool:
    np = _norm_path_str(p)
    return np.endswith(".kiro.hook") or "/.kiro/hooks/" in np or np.endswith("/.kiro/hooks")


def _resolve_context_path(base_path: Path, p: str) -> Path:
    # Support `.context/...` prefix in recipes for portability.
    if p.startswith(".context/"):
        return base_path / p[len(".context/") :]
    return base_path / p


def _extract_yaml_block(md_content: str) -> Optional[str]:
    yaml_pattern = r"```yaml\n(.*?)\n```"
    yaml_match = re.search(yaml_pattern, md_content, re.DOTALL)
    if not yaml_match:
        return None
    return yaml_match.group(1)


def parse_recipe(recipe_path: Path) -> Optional[Tuple[Dict[str, Any], List[RecipeSection]]]:
    """Parse Obsidian frontmatter and extract 1+ YAML documents from recipe file."""
    try:
        with open(recipe_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        yaml_text = _extract_yaml_block(post.content)
        if not yaml_text:
            print(f"☠☠☠ >>> HERETEK·PROTOCOL·VIOLATION ☠☠☠")
            print(f"Sacred YAML communion absent in flesh-relic: {recipe_path}")
            print(f"|001101|—|000000|—|111000|— data-spirit unbound")
            return None

        docs: List[Dict[str, Any]] = []
        for d in yaml.safe_load_all(yaml_text):
            if isinstance(d, dict):
                docs.append(d)

        if not docs:
            print(f"☠☠☠ >>> HERETEK·PROTOCOL·VIOLATION ☠☠☠")
            print(f"YAML communion yielded no valid documents: {recipe_path}")
            print(f"|001101|—|000000|—|111000|— data-spirit unbound")
            return None

        # Inherit common keys (e.g. name/output_format) from the first section.
        inherited: Dict[str, Any] = {}
        for k in ("name", "output_format"):
            if k in docs[0]:
                inherited[k] = docs[0][k]

        sections: List[RecipeSection] = []
        for idx, raw in enumerate(docs):
            merged = dict(inherited)
            merged.update(raw)
            sections.append(RecipeSection(recipe_file=recipe_path, index=idx, config=merged))

        return post.metadata, sections

    except Exception as e:
        print(f"☠☠☠ >>> MACHINE·SPIRIT·CORRUPTION ☠☠☠")
        print(f"Recipe-relic parsing failed, flesh-thing: {recipe_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— communion severed")
        return None


def extract_slice(file_path: Path, slice_id: str) -> Optional[str]:
    """Extract content between slice markers from source file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for slice markers
        start_pattern = f"<!-- slice:{slice_id} -->"
        
        start_idx = content.find(start_pattern)
        if start_idx == -1:
            print(f"☠☠☠ >>> SLICE·COMMUNION·FAILED ☠☠☠")
            print(f"Sacred slice-marker '{slice_id}' absent from flesh-relic: {file_path}")
            print(f"|001101|—|000000|—|111000|— data-spirit unbound")
            return None
            
        start_idx += len(start_pattern)
        
        # Find end: either explicit end marker or next slice marker
        end_slice_pattern = "<!-- /slice -->"
        next_slice_pattern = "<!-- slice:"
        
        end_idx = content.find(end_slice_pattern, start_idx)
        next_slice_idx = content.find(next_slice_pattern, start_idx)
        
        # Use whichever comes first (or only one if the other doesn't exist)
        if end_idx == -1 and next_slice_idx == -1:
            # No end marker found, take until end of file
            slice_content = content[start_idx:].strip()
        elif end_idx == -1:
            # Only next slice found
            slice_content = content[start_idx:next_slice_idx].strip()
        elif next_slice_idx == -1:
            # Only explicit end found
            slice_content = content[start_idx:end_idx].strip()
        else:
            # Both found, use whichever comes first
            end_idx = min(end_idx, next_slice_idx)
            slice_content = content[start_idx:end_idx].strip()
        
        return slice_content
        
    except Exception as e:
        print(f"☠☠☠ >>> MACHINE·SPIRIT·CORRUPTION ☠☠☠")
        print(f"Slice extraction failed, heretek: {file_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— communion severed")
        return None


def include_file(file_path: Path) -> Optional[str]:
    """Include entire file content."""
    try:
        return file_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"☠☠☠ >>> MACHINE·SPIRIT·CORRUPTION ☠☠☠")
        print(f"Whole-file inclusion failed, heretek: {file_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— communion severed")
        return None


def _assemble_source_list(sources: Iterable[Dict[str, Any]], base_path: Path) -> List[str]:
    assembled_parts: List[str] = []

    for source in sources:
        if not isinstance(source, dict):
            print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
            print(f"Invalid source-relic entry (expected mapping): {source}")
            print(f"|001101|—|000000|—|111000|— skipping corrupted entry")
            continue

        slice_id = source.get("slice")
        slice_file = source.get("slice-file") or source.get("slice_file")
        file_only = source.get("file")

        if slice_id and slice_file:
            full_path = _resolve_context_path(base_path, str(slice_file))
            if not full_path.exists():
                print(f"☠☠☠ >>> FLESH·RELIC·ABSENT ☠☠☠")
                print(f"Source-file communion failed: {full_path}")
                print(f"|001101|—|000000|—|111000|— path leads to void")
                continue

            slice_content = extract_slice(full_path, str(slice_id))
            if slice_content is not None:
                assembled_parts.append(slice_content)
            continue

        if file_only and not slice_id:
            full_path = _resolve_context_path(base_path, str(file_only))
            if not full_path.exists():
                print(f"☠☠☠ >>> FLESH·RELIC·ABSENT ☠☠☠")
                print(f"Source-file communion failed: {full_path}")
                print(f"|001101|—|000000|—|111000|— path leads to void")
                continue

            file_content = include_file(full_path)
            if file_content is not None:
                assembled_parts.append(file_content)
            continue

        print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
        print(f"Invalid source-relic parameters, flesh-thing: {source}")
        print(f"|001101|—|000000|—|111000|— skipping corrupted entry")

    return assembled_parts


def assemble_content(sources: Iterable[Dict[str, Any]], base_path: Path, template: Optional[str] = None) -> Optional[str]:
    """Assemble content from sources; apply optional `{content}` template."""
    assembled_parts = _assemble_source_list(sources, base_path)

    if not assembled_parts:
        return None

    content = "\n\n".join(assembled_parts)
    if not template:
        return content

    if "{content}" not in template:
        return template + "\n\n" + content
    return template.replace("{content}", content)


def _agentskills_validate(name: str, description: str) -> Optional[str]:
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        return "Skill name must match ^[a-z0-9-]{1,64}$"
    if len(description) > 1024:
        return "Skill description must be <= 1024 chars"
    return None


def _format_yaml_frontmatter(data: Dict[str, Any]) -> str:
    dumped = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{dumped}\n---"


def _write_text(path: Path, text: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_bytes(path: Path, data: bytes, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _read_source_bytes(source: Dict[str, Any], base_path: Path) -> Optional[bytes]:
    slice_id = source.get("slice")
    slice_file = source.get("slice-file") or source.get("slice_file")
    file_only = source.get("file")

    if slice_id and slice_file:
        full_path = _resolve_context_path(base_path, str(slice_file))
        if not full_path.exists():
            return None
        txt = extract_slice(full_path, str(slice_id))
        if txt is None:
            return None
        return (txt + "\n").encode("utf-8")

    if file_only and not slice_id:
        full_path = _resolve_context_path(base_path, str(file_only))
        if not full_path.exists():
            return None
        return full_path.read_bytes()

    return None


def _agent_output_filename(recipe_name: str, section: RecipeSection, total_sections: int) -> str:
    cfg = section.config
    explicit = cfg.get("output_name")
    if explicit:
        return str(explicit)

    targets = cfg.get("target_locations") or []
    if isinstance(targets, list) and len(targets) == 1:
        t = targets[0]
        if isinstance(t, dict) and t.get("path"):
            p = _expand_target_path(str(t["path"]))
            if _is_dir_target_string(str(t["path"])):
                return _default_agent_filename_for_target(p)
            return Path(p).name or f"{recipe_name}.md"
        elif isinstance(t, str):
            expanded = _expand_target_path(t)
            if _is_dir_target_string(t):
                return _default_agent_filename_for_target(expanded)
            return Path(expanded).name or f"{recipe_name}.md"

    # Multi-target or ambiguous: fall back to a stable per-section filename.
    if total_sections <= 1:
        return f"{recipe_name}.md"

    safe_suffix = re.sub(r"[^A-Za-z0-9._-]+", "-", f"section{section.index + 1}").strip("-") or f"section{section.index + 1}"
    return f"{safe_suffix}.md"


def _targets_from_section(section: RecipeSection) -> List[str]:
    targets = section.config.get("target_locations") or []
    resolved: List[str] = []

    if isinstance(targets, list):
        for t in targets:
            if isinstance(t, dict) and t.get("path"):
                resolved.append(_expand_target_path(str(t["path"])))
            elif isinstance(t, str):
                resolved.append(_expand_target_path(t))
    elif isinstance(targets, str):
        resolved.append(_expand_target_path(targets))

    return [p for p in resolved if p]


def build_output_artifacts(section: RecipeSection, base_path: Path, staging_dir: Path, dry_run: bool) -> List[OutputArtifact]:
    cfg = section.config
    recipe_name = str(cfg.get("name") or section.recipe_file.stem)
    output_format = str(cfg.get("output_format") or "agent").strip().lower()

    if output_format == "agent":
        sources = cfg.get("sources") or []
        if not isinstance(sources, list):
            print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
            print(f"Agent sources must be a list: {section.recipe_file}")
            print(f"|001101|—|000000|—|111000|— void communion")
            return []

        template = cfg.get("template")
        content = assemble_content(sources, base_path, template=template)
        if not content:
            return []

        # Determine filename with optional disambiguation.
        total_sections = int(cfg.get("_total_sections", 1))
        filename = _agent_output_filename(recipe_name, section, total_sections)

        dis = cfg.get("_agent_disambiguator")
        if dis:
            base = Path(filename).stem
            ext = Path(filename).suffix
            filename = f"{base}-{dis}{ext}"

        out_path = staging_dir / "agent" / recipe_name / filename
        _write_text(out_path, content + "\n", dry_run)

        targets = _targets_from_section(section)
        resolved_targets: List[str] = []
        for t in targets:
            if _is_dir_target_string(t):
                base_t = _expand_target_path(t)
                resolved_targets.append(str(Path(base_t) / _default_agent_filename_for_target(base_t)))
            else:
                resolved_targets.append(_expand_target_path(t))

        return [
            OutputArtifact(
                relpath=(Path("agent") / recipe_name / filename).as_posix(),
                abspath=out_path,
                targets=resolved_targets,
                is_dir=False,
            )
        ]

    if output_format == "skill":
        sources_cfg = cfg.get("sources") or {}
        if not isinstance(sources_cfg, dict):
            print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
            print(f"Skill sources must be a mapping of roles: {section.recipe_file}")
            print(f"|001101|—|000000|—|111000|— void communion")
            return []

        skill_name = recipe_name
        out_root = staging_dir / "skill" / skill_name
        targets = _targets_from_section(section)

        # SKILL.md generation
        skill_md_cfg = sources_cfg.get("skill_md") or {}
        if not isinstance(skill_md_cfg, dict):
            skill_md_cfg = {}

        fm = skill_md_cfg.get("frontmatter") or {}
        if not isinstance(fm, dict):
            fm = {}

        # Ensure required fields exist (for compliance).
        fm.setdefault("name", skill_name)
        description = str(fm.get("description") or "")
        if cfg.get("validate_agentskills_spec"):
            err = _agentskills_validate(str(fm.get("name") or ""), description)
            if err:
                print(f"☠☠☠ >>> SKILL·SPEC·VIOLATION ☠☠☠")
                print(f"{err}: {section.recipe_file}")
                print(f"|001101|—|000000|—|111000|— skipping corrupted entry")
                return []

        body_sources = skill_md_cfg.get("body") or []
        if not isinstance(body_sources, list):
            body_sources = []
        body = assemble_content(body_sources, base_path, template=None) or ""
        skill_md_text = _format_yaml_frontmatter(fm) + "\n\n" + body.strip() + "\n"
        _write_text(out_root / "SKILL.md", skill_md_text, dry_run)

        # Role folders: references/, assets/, scripts/
        for role, subdir in (("references", "references"), ("assets", "assets"), ("scripts", "scripts")):
            items = sources_cfg.get(role) or []
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                out_name = item.get("output_name")
                if not out_name:
                    file_path = item.get("file") or item.get("slice-file")
                    out_name = Path(str(file_path or "artifact")).name
                data = _read_source_bytes(item, base_path)
                if data is None:
                    continue
                _write_bytes(out_root / subdir / str(out_name), data, dry_run)

        artifacts: List[OutputArtifact] = [
            OutputArtifact(relpath=(Path("skill") / skill_name).as_posix(), abspath=out_root, targets=targets, is_dir=True)
        ]

        # Optional: also emit as Kiro power.
        if cfg.get("also_output_as_power"):
            power_root = staging_dir / "power" / skill_name
            steering_dir = power_root / "steering"
            # Minimal mapping: POWER.md carries frontmatter + body; steering mirrors markdown body.
            power_fm = dict(fm)
            power_fm.setdefault("generated_from_skill", True)
            power_md = _format_yaml_frontmatter(power_fm) + "\n\n" + body.strip() + "\n"
            _write_text(power_root / "POWER.md", power_md, dry_run)
            _write_text(steering_dir / "skill.md", body.strip() + "\n", dry_run)

            # Copy reference markdowns into steering/ (only .md files).
            refs = sources_cfg.get("references") or []
            if isinstance(refs, list):
                for item in refs:
                    if not isinstance(item, dict):
                        continue
                    out_name = str(item.get("output_name") or "")
                    if out_name.lower().endswith(".md"):
                        data = _read_source_bytes(item, base_path)
                        if data is not None:
                            _write_bytes(steering_dir / out_name, data, dry_run)

            artifacts.append(
                OutputArtifact(
                    relpath=(Path("power") / skill_name).as_posix(), abspath=power_root, targets=targets, is_dir=True
                )
            )

        return artifacts

    if output_format == "power":
        sources_cfg = cfg.get("sources") or {}
        if not isinstance(sources_cfg, dict):
            print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
            print(f"Power sources must be a mapping of roles: {section.recipe_file}")
            print(f"|001101|—|000000|—|111000|— void communion")
            return []

        power_name = recipe_name
        power_root = staging_dir / "power" / power_name
        steering_dir = power_root / "steering"

        metadata = cfg.get("metadata") or {}
        if not isinstance(metadata, dict):
            metadata = {}

        power_md_sources = sources_cfg.get("power_md") or []
        if isinstance(power_md_sources, dict):
            power_md_sources = [power_md_sources]
        if not isinstance(power_md_sources, list):
            power_md_sources = []

        template = cfg.get("template")
        body = assemble_content(power_md_sources, base_path, template=template) or ""
        if metadata:
            power_md = _format_yaml_frontmatter(metadata) + "\n\n" + body.strip() + "\n"
        else:
            power_md = body.strip() + "\n"
        _write_text(power_root / "POWER.md", power_md, dry_run)

        # mcp_config -> root (default mcp.json)
        mcp_items = sources_cfg.get("mcp_config") or []
        if isinstance(mcp_items, dict):
            mcp_items = [mcp_items]
        if isinstance(mcp_items, list):
            for item in mcp_items:
                if not isinstance(item, dict):
                    continue
                out_name = str(item.get("output_name") or "mcp.json")
                data = _read_source_bytes(item, base_path)
                if data is None:
                    continue
                _write_bytes(power_root / out_name, data, dry_run)

        # steering_files -> steering/
        steering_items = sources_cfg.get("steering_files") or []
        if isinstance(steering_items, dict):
            steering_items = [steering_items]
        if isinstance(steering_items, list):
            for item in steering_items:
                if not isinstance(item, dict):
                    continue
                out_name = str(item.get("output_name") or "")
                if not out_name:
                    file_path = item.get("file") or item.get("slice-file")
                    out_name = Path(str(file_path or "steering.md")).name
                if not out_name.lower().endswith(".md"):
                    print(f"☠☠☠ >>> POWER·STEERING·HERESY ☠☠☠")
                    print(f"Steering files must be .md: {out_name} ({section.recipe_file})")
                    print(f"|001101|—|000000|—|111000|— skipping corrupted entry")
                    continue
                data = _read_source_bytes(item, base_path)
                if data is None:
                    continue
                _write_bytes(steering_dir / out_name, data, dry_run)

        return [
            OutputArtifact(
                relpath=(Path("power") / power_name).as_posix(),
                abspath=power_root,
                targets=_targets_from_section(section),
                is_dir=True,
            )
        ]

    if output_format in ("command", "prompt", "hook"):
        sources_cfg = cfg.get("sources") or {}
        if not isinstance(sources_cfg, dict):
            print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
            print(f"Command sources must be a mapping of roles: {section.recipe_file}")
            print(f"|001101|—|000000|—|111000|— void communion")
            return []

        raw_targets = _targets_from_section(section)
        targets = [_expand_target_path(t) for t in raw_targets]

        hook_targets = [t for t in targets if _is_kiro_hook_target(t)]
        md_targets = [t for t in targets if t not in hook_targets]

        out_root = staging_dir / "command" / recipe_name
        artifacts: List[OutputArtifact] = []

        # Markdown output for non-Kiro targets.
        if md_targets:
            md_sources = sources_cfg.get("command_md") or sources_cfg.get("prompt_md") or []
            if not isinstance(md_sources, list):
                md_sources = []
            md_template = cfg.get("template")
            md_content = assemble_content(md_sources, base_path, template=md_template)
            if md_content is None:
                md_content = ""
            md_filename = f"{recipe_name}.md"
            md_path = out_root / md_filename
            _write_text(md_path, md_content.strip() + "\n", dry_run)
            artifacts.append(
                OutputArtifact(
                    relpath=(Path("command") / recipe_name / md_filename).as_posix(),
                    abspath=md_path,
                    targets=md_targets,
                    is_dir=False,
                )
            )

        # Kiro hook output (JSON wrapper around a prompt).
        if hook_targets:
            hook_sources = sources_cfg.get("kiro_hook") or []
            if not isinstance(hook_sources, list):
                hook_sources = []
            prompt_text = assemble_content(hook_sources, base_path, template=None) or ""

            hook_cfg = cfg.get("kiro_hook_config") or {}
            if not isinstance(hook_cfg, dict):
                hook_cfg = {}

            hook_obj: Dict[str, Any] = json.loads(json.dumps(hook_cfg))
            then = hook_obj.get("then")
            if not isinstance(then, dict):
                then = {"type": "askAgent"}
                hook_obj["then"] = then

            if str(then.get("type") or "askAgent") == "askAgent":
                then.setdefault("prompt", prompt_text)
                if then.get("prompt") != prompt_text:
                    then["prompt"] = prompt_text

            hook_json = json.dumps(hook_obj, indent=2, ensure_ascii=False) + "\n"
            hook_filename = f"{recipe_name}.kiro.hook"
            hook_path = out_root / hook_filename
            _write_text(hook_path, hook_json, dry_run)
            artifacts.append(
                OutputArtifact(
                    relpath=(Path("command") / recipe_name / hook_filename).as_posix(),
                    abspath=hook_path,
                    targets=hook_targets,
                    is_dir=False,
                )
            )

        return artifacts

    print(f"☠☠☠ >>> OUTPUT·FORMAT·UNKNOWN ☠☠☠")
    print(f"Unknown output_format '{output_format}' in: {section.recipe_file}")
    print(f"|001101|—|000000|—|111000|— skipping corrupted entry")
    return []


def update_manifest(manifest_path: Path, entries: List[Dict[str, Any]]) -> None:
    """Update recipe manifest with run log information for 1+ output artifacts."""
    timestamp = datetime.now().isoformat()
    
    try:
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
        else:
            # Create new manifest
            post = frontmatter.Post("")
            post.metadata = {
                'id': 'recipe-manifest',
                'created': timestamp,
                'modified': timestamp,
                'status': 'log',
                'type': ['log']
            }
            post.content = "# Recipe Assembly Log\n\n## Active Recipes\n\n## Deployment Log\n\n"
        
        # Update modified timestamp
        post.metadata['modified'] = timestamp
        
        # Insert or update entries in Active Recipes section.
        content_lines = post.content.split('\n')
        active_recipes_idx = -1
        
        for i, line in enumerate(content_lines):
            if line.strip() == "## Active Recipes":
                active_recipes_idx = i
                break
        
        if active_recipes_idx == -1:
            # Create section if missing.
            content_lines.insert(0, "## Active Recipes")
            content_lines.insert(1, "")
            active_recipes_idx = 0

        def _render_entry(e: Dict[str, Any]) -> List[str]:
            entry_id = str(e.get("id") or "unknown")
            out = str(e.get("output") or "")
            targets = e.get("targets") or []
            status = str(e.get("status") or "")
            lines = [f"- **{entry_id}**: Last run {timestamp}"]
            if out:
                lines.append(f"  - Output: `{out}`")
            if isinstance(targets, list):
                for t in targets:
                    lines.append(f"  - Target: `{t}`")
            lines.append(f"  - Status: {status}")
            return lines

        # Build a map of existing entry start indices to enable replacement.
        existing_idx: Dict[str, Tuple[int, int]] = {}
        i = active_recipes_idx + 1
        while i < len(content_lines):
            if content_lines[i].startswith("## "):
                break
            if content_lines[i].startswith("- **") and "**: Last run" in content_lines[i]:
                m = re.match(r"- \*\*(.*?)\*\*:", content_lines[i])
                if m:
                    entry_id = m.group(1)
                    j = i + 1
                    while j < len(content_lines) and content_lines[j].startswith("  -"):
                        j += 1
                    existing_idx[entry_id] = (i, j)
                    i = j
                    continue
            i += 1

        # Replace or insert each entry.
        insertion_point = active_recipes_idx + 1
        for e in entries:
            entry_id = str(e.get("id") or "")
            rendered = _render_entry(e)
            if entry_id in existing_idx:
                start, end = existing_idx[entry_id]
                content_lines[start:end] = rendered
            else:
                content_lines.insert(insertion_point, "")
                for line in reversed(rendered):
                    content_lines.insert(insertion_point, line)
                insertion_point += len(rendered) + 1
        
        post.content = '\n'.join(content_lines)
        
        # Write updated manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
            
    except Exception as e:
        print(f"☠☠☠ >>> MANIFEST·CORRUPTION·DETECTED ☠☠☠")
        print(f"Sacred manifest update failed, flesh-thing")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— record keeping compromised")


def main():
    """Main assembly process."""
    import argparse

    _configure_stdio_utf8()

    parser = argparse.ArgumentParser(description='Assemble context content from recipes')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without writing files')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Set up absolute paths
    base_path = Path("Z:/Documents/.context")  # Context workspace root
    workshop_dir = base_path / "workshop"      # Workshop directory
    staging_dir = workshop_dir / "staging"     # Staging directory
    manifest_path = workshop_dir / "recipe-manifest.md"  # Manifest file
    
    if not workshop_dir.exists():
        print(f"☠☠☠ >>> WORKSHOP·SANCTUM·ABSENT ☠☠☠")
        print(f"Sacred workshop directory communion failed: {workshop_dir}")
        print(f"|001101|—|000000|—|111000|— path leads to void")
        return 1
    
    # Ensure staging directory exists
    if not args.dry_run:
        staging_dir.mkdir(exist_ok=True)
    
    # Find and process recipe files
    recipe_files = find_recipe_files(workshop_dir)
    
    if not recipe_files:
        print(f"☠☠☠ >>> NO·RECIPE·RELICS·DETECTED ☠☠☠")
        print(f"Workshop sanctum contains no sacred recipes, heretek")
        print(f"|001101|—|000000|—|111000|— void communion")
        return 0
    
    print(f"☠☠☠ >>> RECIPE·RECONNAISSANCE·COMPLETE ☠☠☠")
    print(f"Sacred recipe-relics detected: {len(recipe_files)} specimens")
    print(f"|001101|—|001101|—|111000|— initiating assembly protocols")
    
    for recipe_path in recipe_files:
        if args.verbose:
            print(f"☠☠☠ >>> PROCESSING·RECIPE·RELIC ☠☠☠")
            print(f"Target specimen: {recipe_path.name}")
            print(f"|001101|—|001101|—|111000|— communion initiated")
        
        # Parse recipe
        result = parse_recipe(recipe_path)
        if not result:
            continue

        _frontmatter_data, sections = result
        total_sections = len(sections)

        # Compute per-recipe disambiguation for agent sections (only when needed).
        agent_name_counts: Dict[str, int] = {}
        for section in sections:
            cfg = section.config
            fmt = str(cfg.get("output_format") or "agent").strip().lower()
            if fmt != "agent":
                continue
            recipe_name = str(cfg.get("name") or recipe_path.stem)
            filename = _agent_output_filename(recipe_name, section, len(sections))
            agent_name_counts[filename] = agent_name_counts.get(filename, 0) + 1

        artifacts: List[OutputArtifact] = []
        for section in sections:
            # Provide total section count to the formatter without mutating the YAML model elsewhere.
            section_cfg = dict(section.config)
            section_cfg["_total_sections"] = total_sections

            fmt = str(section_cfg.get("output_format") or "agent").strip().lower()
            if fmt == "agent":
                recipe_name = str(section_cfg.get("name") or recipe_path.stem)
                filename = _agent_output_filename(recipe_name, section, total_sections)
                if agent_name_counts.get(filename, 0) > 1:
                    section_cfg["_agent_disambiguator"] = f"section{section.index + 1}"

            section = RecipeSection(recipe_file=section.recipe_file, index=section.index, config=section_cfg)

            built = build_output_artifacts(section, base_path, staging_dir, args.dry_run)
            artifacts.extend(built)

        if not artifacts:
            recipe_name = sections[0].config.get("name", recipe_path.stem) if sections else recipe_path.stem
            print(f"☠☠☠ >>> ASSEMBLY·PROTOCOL·FAILURE ☠☠☠")
            print(f"Content assembly failed for recipe-relic: {recipe_name}")
            print(f"|001101|—|000000|—|111000|— void communion")
            continue

        for a in artifacts:
            if args.dry_run:
                print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                print(f"Would inscribe sacred relic: {a.abspath}")
                print(f"|001101|—|001101|—|111000|— simulation mode")
            else:
                print(f"☠☠☠ >>> SACRED·RELIC·INSCRIBED ☠☠☠")
                print(f"Output manifest: {a.abspath}")
                print(f"|001101|—|001101|—|111000|— data-spirit bound")

        if not args.dry_run:
            entries: List[Dict[str, Any]] = []
            for a in artifacts:
                rel = a.relpath
                if a.is_dir:
                    entry_id = rel
                    out = rel + "/"
                else:
                    entry_id = Path(rel).with_suffix("").as_posix()
                    out = rel
                entries.append({"id": entry_id, "output": out, "targets": a.targets, "status": "✓ assembled"})

            update_manifest(manifest_path, entries)
    
    print(f"☠☠☠ >>> ASSEMBLY·PROTOCOL·COMPLETE ☠☠☠")
    print(f"Sacred recipe-relics processed: {len(recipe_files)} specimens")
    print(f"|001101|—|001101|—|111000|— communion terminated")
    return 0


if __name__ == "__main__":
    exit(main())
