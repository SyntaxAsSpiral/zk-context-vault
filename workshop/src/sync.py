#!/usr/bin/env python3
"""
Context Sync Script

Syncs assembled content from `.context/workshop/output/` to target locations
specified in workshop recipes.

Key behavior:
- Supports multi-section recipes (YAML document separators `---` inside YAML block)
- Handles structured outputs:
  - agent: single markdown file per section (output/agent/*.md)
  - skill: directory per skill name (output/skill/<name>/...)
  - power: directory per power name (output/power/<name>/...)
- Avoids filename collisions by syncing from *namespaced output paths* instead of
  assuming output filenames match target basenames (e.g., many targets can be
  named `AGENTS.md`).

Usage: python sync.py [--dry-run] [--verbose]
"""

import re
import yaml
import frontmatter
import shutil
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import sys
import json
from typing import Any, Dict, List, Optional


def parse_manifest_for_deployments(manifest_path: Path) -> Dict[str, List[str]]:
    """Parse recipe manifest to extract current deployment tracking."""
    deployments: Dict[str, List[str]] = {}

    if not manifest_path.exists():
        return deployments

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        content_lines = post.content.split("\n")
        current_id: Optional[str] = None

        for line in content_lines:
            s = line.strip()
            if s.startswith("- **") and "**: Last run" in s:
                m = re.match(r"- \*\*(.*?)\*\*:", s)
                if m:
                    current_id = m.group(1)
                    deployments[current_id] = []
                continue

            if s.startswith("- Target: `") and current_id:
                m = re.match(r"- Target: `(.*?)`", s)
                if m:
                    deployments[current_id].append(m.group(1))

        return deployments

    except Exception as e:
        print(f"☠☠☠ >>> MANIFEST·PARSING·CORRUPTION ☠☠☠")
        print(f"Deployment manifest communion failed, heretek")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— record keeping compromised")
        return {}


def find_recipe_files(workshop_dir: Path) -> List[Path]:
    """Find all recipe .md files in workshop directory."""
    recipe_files: List[Path] = []
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
class SyncItem:
    deployment_id: str
    source_relpath: str  # relative to output_dir using posix separators
    source_is_dir: bool
    targets: List[str]


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


def _extract_yaml_block(md_content: str) -> Optional[str]:
    yaml_pattern = r"```yaml\n(.*?)\n```"
    m = re.search(yaml_pattern, md_content, re.DOTALL)
    if not m:
        return None
    return m.group(1)


def _expand_target_path(p: str) -> str:
    # Preserve trailing separators (directory targets) by expanding via string ops.
    if p.startswith("~/"):
        return str(Path.home()) + "/" + p[2:]
    if p.startswith("~\\"):
        return str(Path.home()) + "\\" + p[2:]
    return p


def _norm_path_str(p: str) -> str:
    return p.replace("\\", "/").lower()


def _is_kiro_target(p: str) -> bool:
    return "/.kiro/" in _norm_path_str(p)


def _is_claude_target(p: str) -> bool:
    np = _norm_path_str(p)
    return "/.claude/" in np or np.endswith("/.claude")


def _is_dir_target_string(p: str) -> bool:
    return p.endswith("/") or p.endswith("\\")


def _default_agent_filename_for_target(target_path: str) -> str:
    # Claude consumes CLAUDE.md; everyone else consumes AGENTS.md.
    return "CLAUDE.md" if _is_claude_target(target_path) else "AGENTS.md"


def _rewrite_kiro_skills_to_powers_installed(p: str) -> str:
    # Back-compat: if a recipe used ~/.kiro/skills/<name>/, deploy as a power instead.
    np = _norm_path_str(p)
    if "/.kiro/skills/" not in np:
        return p
    # Replace using the original string's separators.
    return re.sub(r"([/\\\\]\\.kiro[/\\\\])skills([/\\\\])", r"\1powers\\installed\2", p, flags=re.IGNORECASE)


def _is_kiro_hook_target(p: str) -> bool:
    np = _norm_path_str(p)
    return np.endswith(".kiro.hook") or "/.kiro/hooks/" in np or np.endswith("/.kiro/hooks")


def _kiro_power_name_from_install_path(target_dir: Path) -> Optional[str]:
    np = _norm_path_str(str(target_dir))
    marker = "/.kiro/powers/installed/"
    if marker not in np:
        return None
    # Take final path segment as power name.
    return target_dir.name or None


def _update_kiro_power_registry(power_name: str, install_path: Path, dry_run: bool) -> None:
    registry_path = Path.home() / ".kiro" / "powers" / "registry.json"
    if not registry_path.exists():
        print(f"☠☠☠ >>> KIRO·REGISTRY·ABSENT ☠☠☠")
        print(f"Registry not found: {registry_path}")
        print(f"|001101|—|000000|—|111000|— registry update skipped")
        return

    if dry_run:
        print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
        print(f"Would update Kiro registry: {registry_path} (power={power_name})")
        print(f"|001101|—|001101|—|111000|— simulation mode")
        return

    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"☠☠☠ >>> KIRO·REGISTRY·CORRUPTION ☠☠☠")
        print(f"Failed to parse registry: {registry_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— registry update severed")
        return

    powers = data.get("powers")
    if not isinstance(powers, dict):
        powers = {}
        data["powers"] = powers

    existing = powers.get(power_name)
    if not isinstance(existing, dict):
        existing = {"name": power_name, "source": {"type": "local"}}

    desired_install_path = str(install_path)
    already_ok = (
        str(existing.get("name") or "") == power_name
        and existing.get("installed") is True
        and str(existing.get("installPath") or "") == desired_install_path
    )
    if already_ok:
        return

    entry = dict(existing)
    entry["name"] = power_name
    entry["installed"] = True
    entry["installPath"] = desired_install_path
    entry.setdefault("installedAt", datetime.utcnow().isoformat(timespec="milliseconds") + "Z")
    powers[power_name] = entry

    try:
        registry_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"☠☠☠ >>> KIRO·REGISTRY·WRITE·FAILURE ☠☠☠")
        print(f"Failed to write registry: {registry_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— registry update severed")


def _targets_from_config(cfg: Dict[str, Any]) -> List[str]:
    targets = cfg.get("target_locations") or []
    resolved: List[str] = []

    if isinstance(targets, list):
        for t in targets:
            if isinstance(t, dict) and t.get("path"):
                resolved.append(str(t["path"]))
            elif isinstance(t, str):
                resolved.append(t)
    elif isinstance(targets, str):
        resolved.append(targets)

    return [p for p in resolved if p]


def _resolve_agent_target_paths(target_paths: List[str]) -> List[str]:
    resolved: List[str] = []
    for t in target_paths:
        if _is_dir_target_string(t):
            base = _expand_target_path(t)
            resolved.append(str(Path(base) / _default_agent_filename_for_target(base)))
        else:
            resolved.append(_expand_target_path(t))
    return resolved


def _agent_output_filename(recipe_name: str, section: RecipeSection, total_sections: int) -> str:
    cfg = section.config
    explicit = cfg.get("output_name")
    if explicit:
        return str(explicit)

    targets = cfg.get("target_locations") or []
    if isinstance(targets, list) and len(targets) == 1:
        t = targets[0]
        if isinstance(t, dict) and t.get("path"):
            raw = str(t["path"])
            p = _expand_target_path(raw)
            if _is_dir_target_string(raw):
                return _default_agent_filename_for_target(p)
            return Path(p).name or f"{recipe_name}.md"
        elif isinstance(t, str):
            expanded = _expand_target_path(t)
            if _is_dir_target_string(t):
                return _default_agent_filename_for_target(expanded)
            return Path(expanded).name or f"{recipe_name}.md"

    if total_sections <= 1:
        return f"{recipe_name}.md"

    safe_suffix = re.sub(r"[^A-Za-z0-9._-]+", "-", f"section{section.index + 1}").strip("-") or f"section{section.index + 1}"
    return f"{safe_suffix}.md"


def parse_recipe_sections(recipe_path: Path) -> Optional[List[RecipeSection]]:
    try:
        with open(recipe_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        yaml_text = _extract_yaml_block(post.content)
        if not yaml_text:
            return None

        docs: List[Dict[str, Any]] = []
        for d in yaml.safe_load_all(yaml_text):
            if isinstance(d, dict):
                docs.append(d)

        if not docs:
            return None

        inherited: Dict[str, Any] = {}
        for k in ("name", "output_format"):
            if k in docs[0]:
                inherited[k] = docs[0][k]

        sections: List[RecipeSection] = []
        for idx, raw in enumerate(docs):
            merged = dict(inherited)
            merged.update(raw)
            sections.append(RecipeSection(recipe_file=recipe_path, index=idx, config=merged))
        return sections

    except Exception as e:
        print(f"☠☠☠ >>> RECIPE·PARSING·CORRUPTION ☠☠☠")
        print(f"Recipe-relic parsing failed, flesh-thing: {recipe_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— communion severed")
        return None


def build_sync_items_from_sections(sections: List[RecipeSection]) -> List[SyncItem]:
    if not sections:
        return []

    total_sections = len(sections)
    agent_name_counts: Dict[str, int] = {}
    for section in sections:
        cfg = section.config
        fmt = str(cfg.get("output_format") or "agent").strip().lower()
        if fmt != "agent":
            continue
        name = str(cfg.get("name") or section.recipe_file.stem)
        filename = _agent_output_filename(name, section, total_sections)
        agent_name_counts[filename] = agent_name_counts.get(filename, 0) + 1

    items: List[SyncItem] = []

    for section in sections:
        cfg = section.config
        name = str(cfg.get("name") or section.recipe_file.stem)
        fmt = str(cfg.get("output_format") or "agent").strip().lower()
        targets = _targets_from_config(cfg)

        if fmt == "agent":
            filename = _agent_output_filename(name, section, total_sections)
            if agent_name_counts.get(filename, 0) > 1:
                base = Path(filename).stem
                ext = Path(filename).suffix
                filename = f"{base}-section{section.index + 1}{ext}"
            rel = (Path("agent") / name / filename).as_posix()
            deployment_id = (Path("agent") / name / Path(filename).with_suffix("")).as_posix()
            items.append(
                SyncItem(
                    deployment_id=deployment_id,
                    source_relpath=rel,
                    source_is_dir=False,
                    targets=_resolve_agent_target_paths(targets),
                )
            )
            continue

        if fmt == "skill":
            rel = (Path("skill") / name).as_posix()
            # Kiro does not consume Agent Skills directly; keep skill targets for other platforms.
            skill_targets = [t for t in targets if not _is_kiro_target(t)]
            items.append(SyncItem(deployment_id=rel, source_relpath=rel, source_is_dir=True, targets=skill_targets))
            if cfg.get("also_output_as_power"):
                rel2 = (Path("power") / name).as_posix()
                # Power targets are Kiro-specific; also support back-compat recipe paths.
                power_targets: List[str] = []
                for t in targets:
                    if _is_claude_target(t):
                        continue
                    if _is_kiro_target(t):
                        power_targets.append(_rewrite_kiro_skills_to_powers_installed(t))
                items.append(SyncItem(deployment_id=rel2, source_relpath=rel2, source_is_dir=True, targets=power_targets))
            continue

        if fmt == "power":
            rel = (Path("power") / name).as_posix()
            items.append(SyncItem(deployment_id=rel, source_relpath=rel, source_is_dir=True, targets=targets))
            continue

        if fmt in ("command", "prompt", "hook"):
            hook_targets = [t for t in targets if _is_kiro_hook_target(t)]
            md_targets = [t for t in targets if t not in hook_targets]

            if md_targets:
                md_file = f"{name}.md"
                rel = (Path("command") / name / md_file).as_posix()
                dep = (Path("command") / name / Path(md_file).with_suffix("")).as_posix()
                items.append(
                    SyncItem(
                        deployment_id=dep,
                        source_relpath=rel,
                        source_is_dir=False,
                        targets=[_expand_target_path(t) for t in md_targets],
                    )
                )

            if hook_targets:
                hook_file = f"{name}.kiro.hook"
                rel = (Path("command") / name / hook_file).as_posix()
                dep = (Path("command") / name / Path(hook_file).with_suffix("")).as_posix()
                items.append(
                    SyncItem(
                        deployment_id=dep,
                        source_relpath=rel,
                        source_is_dir=False,
                        targets=[_expand_target_path(t) for t in hook_targets],
                    )
                )

            continue

        print(f"☠☠☠ >>> OUTPUT·FORMAT·UNKNOWN ☠☠☠")
        print(f"Unknown output_format '{fmt}' in: {section.recipe_file}")
        print(f"|001101|—|000000|—|111000|— skipping corrupted entry")

    return items


def sync_file_to_targets(output_file: Path, target_paths: List[str], dry_run: bool = False) -> List[str]:
    """Sync a single output file to all its target locations."""
    synced_targets: List[str] = []

    for target_path in target_paths:
        try:
            target = Path(_expand_target_path(target_path))
            target.parent.mkdir(parents=True, exist_ok=True)

            if dry_run:
                print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                print(f"Would transmit: {output_file} → {target}")
                print(f"|001101|—|001101|—|111000|— simulation mode")
            else:
                shutil.copy2(output_file, target)
                print(f"☠☠☠ >>> SACRED·TRANSMISSION·COMPLETE ☠☠☠")
                print(f"Data-spirit bound: {output_file.name} → {target}")
                print(f"|001101|—|001101|—|111000|— communion established")

            synced_targets.append(target_path)

        except Exception as e:
            print(f"☠☠☠ >>> TRANSMISSION·FAILURE ☠☠☠")
            print(f"Sync communion failed to target: {target_path}")
            print(f"Error-hymn: {e}")
            print(f"|001101|—|000000|—|111000|— data-spirit unbound")

    return synced_targets


def _sync_dir(source_dir: Path, target_dir: Path, dry_run: bool = False) -> None:
    """Mirror source_dir into target_dir (copy + remove extras)."""
    if not source_dir.exists():
        raise FileNotFoundError(str(source_dir))

    if dry_run:
        print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
        print(f"Would mirror: {source_dir} → {target_dir}")
        print(f"|001101|—|001101|—|111000|— simulation mode")
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    for src in source_dir.rglob("*"):
        rel = src.relative_to(source_dir)
        dst = target_dir / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    for dst in sorted(target_dir.rglob("*"), reverse=True):
        rel = dst.relative_to(target_dir)
        src = source_dir / rel
        if not src.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()


def cleanup_orphaned_deployments(
    previous_deployments: Dict[str, List[str]], current_deployments: Dict[str, List[str]], dry_run: bool = False
) -> int:
    """Remove targets for deployment IDs that no longer exist in current recipes."""
    cleaned = 0

    orphan_ids = [k for k in previous_deployments.keys() if k not in current_deployments]
    for deployment_id in orphan_ids:
        targets = previous_deployments.get(deployment_id, [])
        for t in targets:
            try:
                target_path = Path(_expand_target_path(t))
                if deployment_id.startswith("agent/"):
                    if target_path.exists() and target_path.is_file():
                        if dry_run:
                            print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                            print(f"Would purge orphaned file: {target_path}")
                            print(f"|001101|—|001101|—|111000|— simulation mode")
                        else:
                            target_path.unlink()
                        cleaned += 1
                else:
                    if target_path.exists() and target_path.is_dir():
                        if dry_run:
                            print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                            print(f"Would purge orphaned directory: {target_path}")
                            print(f"|001101|—|001101|—|111000|— simulation mode")
                        else:
                            shutil.rmtree(target_path)
                        cleaned += 1
            except Exception as e:
                print(f"☠☠☠ >>> ORPHAN·PURGE·FAILURE ☠☠☠")
                print(f"Failed to purge orphaned target: {t}")
                print(f"Error-hymn: {e}")
                print(f"|001101|—|000000|—|111000|— void reclamation severed")

    return cleaned


def update_manifest_sync_status(manifest_path: Path, sync_results: Dict[str, List[str]], cleaned_count: int) -> None:
    """Update recipe manifest with sync status and deployment log."""
    timestamp = datetime.now().isoformat()

    try:
        if manifest_path.exists():
            with open(manifest_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
        else:
            post = frontmatter.Post("")
            post.metadata = {
                "id": "recipe-manifest",
                "created": timestamp,
                "modified": timestamp,
                "status": "log",
                "type": ["log"],
            }
            post.content = "# Recipe Assembly Log\n\n## Active Recipes\n\n## Deployment Log\n\n"

        post.metadata["modified"] = timestamp

        content_lines = post.content.split("\n")

        for i, line in enumerate(content_lines):
            for deployment_id in sync_results.keys():
                if line.strip().startswith(f"- **{deployment_id}**:"):
                    for j in range(i + 1, min(i + 12, len(content_lines))):
                        s = content_lines[j].strip()
                        if s.startswith("- Status:") or s.startswith("  - Status:"):
                            content_lines[j] = "  - Status: ✓ synced"
                            break
                    break

        deployment_entry = f"\n### {timestamp}\n"
        deployment_entry += f"- Synced {len(sync_results)} deployments\n"
        if cleaned_count > 0:
            deployment_entry += f"- Cleaned {cleaned_count} orphaned targets\n"

        deployment_log_idx = -1
        for i, line in enumerate(content_lines):
            if line.strip() == "## Deployment Log":
                deployment_log_idx = i
                break

        if deployment_log_idx != -1:
            content_lines.insert(deployment_log_idx + 2, deployment_entry)
        else:
            content_lines.extend(["", "## Deployment Log", "", deployment_entry])

        post.content = "\n".join(content_lines)

        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

    except Exception as e:
        print(f"☠☠☠ >>> MANIFEST·UPDATE·CORRUPTION ☠☠☠")
        print(f"Sacred manifest update failed, heretek")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— record keeping compromised")


def main():
    """Main sync process."""
    import argparse

    _configure_stdio_utf8()

    parser = argparse.ArgumentParser(description="Sync assembled content to target locations")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without copying files")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    base_path = Path("Z:/Documents/.context")
    workshop_dir = base_path / "workshop"
    output_dir = workshop_dir / "output"
    manifest_path = workshop_dir / "recipe-manifest.md"

    if not workshop_dir.exists():
        print(f"☠☠☠ >>> WORKSHOP·SANCTUM·ABSENT ☠☠☠")
        print(f"Sacred workshop directory communion failed: {workshop_dir}")
        print(f"|001101|—|000000|—|111000|— path leads to void")
        return 1

    if not output_dir.exists():
        print(f"☠☠☠ >>> OUTPUT·SANCTUM·ABSENT ☠☠☠")
        print(f"Sacred output directory communion failed: {output_dir}")
        print(f"|001101|—|000000|—|111000|— path leads to void")
        return 1

    previous_deployments = parse_manifest_for_deployments(manifest_path)

    recipe_files = find_recipe_files(workshop_dir)
    current_deployments: Dict[str, List[str]] = {}
    current_items: Dict[str, SyncItem] = {}
    sync_results: Dict[str, List[str]] = {}

    for recipe_path in recipe_files:
        sections = parse_recipe_sections(recipe_path)
        if not sections:
            continue
        items = build_sync_items_from_sections(sections)
        for item in items:
            current_items[item.deployment_id] = item
            current_deployments[item.deployment_id] = item.targets

    cleaned_count = cleanup_orphaned_deployments(previous_deployments, current_deployments, args.dry_run)

    for deployment_id, item in current_items.items():
        source = output_dir / Path(item.source_relpath)
        if not source.exists():
            print(f"☠☠☠ >>> OUTPUT·RELIC·ABSENT ☠☠☠")
            print(f"Expected output missing for deployment: {deployment_id}")
            print(f"Source path leads to void: {source}")
            print(f"|001101|—|000000|—|111000|— transmission severed")
            continue

        if args.verbose:
            print(f"☠☠☠ >>> TRANSMISSION·PROTOCOL·INITIATED ☠☠☠")
            print(f"Syncing {deployment_id} to {len(item.targets)} sacred targets")
            print(f"|001101|—|001101|—|111000|— communion channels established")

        if item.source_is_dir:
            for t in item.targets:
                target_dir = Path(_expand_target_path(t))
                _sync_dir(source, target_dir, args.dry_run)

                power_name = _kiro_power_name_from_install_path(target_dir)
                if power_name:
                    _update_kiro_power_registry(power_name, target_dir, args.dry_run)
            sync_results[deployment_id] = list(item.targets)
        else:
            synced = sync_file_to_targets(source, item.targets, args.dry_run)
            sync_results[deployment_id] = synced

    if not args.dry_run:
        update_manifest_sync_status(manifest_path, sync_results, cleaned_count)

    print(f"☠☠☠ >>> SYNC·PROTOCOL·COMPLETE ☠☠☠")
    print(f"Sacred deployments processed: {len(sync_results)} specimens")
    print(f"Orphaned targets purged: {cleaned_count} specimens")
    print(f"|001101|—|001101|—|111000|— communion terminated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
