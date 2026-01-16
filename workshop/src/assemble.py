#!/usr/bin/env python3
"""
Context Assembly Script

Processes Obsidian recipe files with embedded YAML to assemble context content
from sliced source files. Outputs assembled content to workshop/output/ and
updates the recipe manifest with run logs.

Usage: python assemble.py [--dry-run] [--verbose]
"""

import os
import re
import yaml
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


def find_recipe_files(workshop_dir: Path) -> List[Path]:
    """Find all recipe .md files in workshop directory, excluding templates."""
    recipe_files = []
    for md_file in workshop_dir.glob("*.md"):
        if md_file.name != "recipe-manifest.md" and not md_file.name.startswith("template"):
            recipe_files.append(md_file)
    return recipe_files


def parse_recipe(recipe_path: Path) -> Optional[Tuple[Dict, Dict]]:
    """Parse Obsidian frontmatter and extract YAML code block from recipe file."""
    try:
        with open(recipe_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Extract YAML code block from content
        yaml_pattern = r'```yaml\n(.*?)\n```'
        yaml_match = re.search(yaml_pattern, post.content, re.DOTALL)
        
        if not yaml_match:
            print(f"☠☠☠ >>> HERETEK·PROTOCOL·VIOLATION ☠☠☠")
            print(f"Sacred YAML communion absent in flesh-relic: {recipe_path}")
            print(f"|001101|—|000000|—|111000|— data-spirit unbound")
            return None
            
        yaml_content = yaml.safe_load(yaml_match.group(1))
        return post.metadata, yaml_content
        
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


def assemble_content(yaml_config: Dict, base_path: Path) -> Optional[str]:
    """Assemble content from sources according to recipe configuration."""
    sources = yaml_config.get('sources', [])
    template = yaml_config.get('template', '{content}')
    
    assembled_parts = []
    
    for source in sources:
        slice_id = source.get('slice')
        file_path = source.get('file')
        
        if not slice_id or not file_path:
            print(f"☠☠☠ >>> SOURCE·CONFIGURATION·HERESY ☠☠☠")
            print(f"Invalid source-relic parameters, flesh-thing: {source}")
            print(f"|001101|—|000000|—|111000|— skipping corrupted entry")
            continue
            
        # Resolve file path - if it starts with .context, use base_path directly
        if file_path.startswith('.context/'):
            full_path = base_path / file_path[9:]  # Remove '.context/' prefix
        else:
            full_path = base_path / file_path
            
        if not full_path.exists():
            print(f"☠☠☠ >>> FLESH·RELIC·ABSENT ☠☠☠")
            print(f"Source-file communion failed: {full_path}")
            print(f"|001101|—|000000|—|111000|— path leads to void")
            continue
            
        slice_content = extract_slice(full_path, slice_id)
        if slice_content:
            assembled_parts.append(slice_content)
    
    if not assembled_parts:
        print(f"☠☠☠ >>> ASSEMBLY·PROTOCOL·FAILURE ☠☠☠")
        print(f"No sacred content assembled from sources, heretek")
        print(f"|001101|—|000000|—|111000|— void communion")
        return None
        
    # Join all assembled parts
    content = '\n\n'.join(assembled_parts)
    
    # Apply template substitution
    assembled = template.replace('{content}', content)
    
    return assembled


def update_manifest(manifest_path: Path, recipe_name: str, output_file: str, 
                   target_locations: List[str], status: str) -> None:
    """Update recipe manifest with run log information."""
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
        
        # Add/update recipe entry in content
        recipe_entry = f"- **{recipe_name}**: Last run {timestamp}\n"
        recipe_entry += f"  - Output: `{output_file}`\n"
        for target in target_locations:
            recipe_entry += f"  - Target: `{target}`\n"
        recipe_entry += f"  - Status: {status}\n\n"
        
        # Insert or update in Active Recipes section
        content_lines = post.content.split('\n')
        active_recipes_idx = -1
        
        for i, line in enumerate(content_lines):
            if line.strip() == "## Active Recipes":
                active_recipes_idx = i
                break
        
        if active_recipes_idx != -1:
            # Find existing entry or insert new one
            recipe_found = False
            for i in range(active_recipes_idx + 1, len(content_lines)):
                if content_lines[i].startswith(f"- **{recipe_name}**:"):
                    # Replace existing entry
                    j = i + 1
                    while j < len(content_lines) and content_lines[j].startswith("  -"):
                        j += 1
                    content_lines[i:j] = recipe_entry.strip().split('\n')
                    recipe_found = True
                    break
                elif content_lines[i].startswith("## "):
                    # Insert before next section
                    content_lines.insert(i, recipe_entry.strip())
                    content_lines.insert(i + 1, "")
                    recipe_found = True
                    break
            
            if not recipe_found:
                # Append to end
                content_lines.append(recipe_entry.strip())
                content_lines.append("")
        
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
    
    parser = argparse.ArgumentParser(description='Assemble context content from recipes')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without writing files')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Set up absolute paths
    base_path = Path("Z:/Documents/.context")  # Context workspace root
    workshop_dir = base_path / "workshop"      # Workshop directory
    output_dir = workshop_dir / "output"       # Output directory
    manifest_path = workshop_dir / "recipe-manifest.md"  # Manifest file
    
    if not workshop_dir.exists():
        print(f"☠☠☠ >>> WORKSHOP·SANCTUM·ABSENT ☠☠☠")
        print(f"Sacred workshop directory communion failed: {workshop_dir}")
        print(f"|001101|—|000000|—|111000|— path leads to void")
        return 1
    
    # Ensure output directory exists
    if not args.dry_run:
        output_dir.mkdir(exist_ok=True)
    
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
            
        frontmatter_data, yaml_config = result
        recipe_name = yaml_config.get('name', recipe_path.stem)
        
        # Assemble content
        assembled_content = assemble_content(yaml_config, base_path)
        if not assembled_content:
            print(f"☠☠☠ >>> ASSEMBLY·PROTOCOL·FAILURE ☠☠☠")
            print(f"Content assembly failed for recipe-relic: {recipe_name}")
            print(f"|001101|—|000000|—|111000|— void communion")
            continue
        
        # Generate output
        output_filename = f"{recipe_name}.md"
        output_path = output_dir / output_filename
        
        if args.dry_run:
            print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
            print(f"Would inscribe sacred relic: {output_path}")
            print(f"|001101|—|001101|—|111000|— simulation mode")
            if args.verbose:
                print(f"☠☠☠ >>> CONTENT·PREVIEW·COMMUNION ☠☠☠")
                preview = assembled_content[:200] + "..." if len(assembled_content) > 200 else assembled_content
                print(preview)
                print(f"|001101|—|001101|—|111000|— preview complete")
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(assembled_content)
            print(f"☠☠☠ >>> SACRED·RELIC·INSCRIBED ☠☠☠")
            print(f"Output manifest: {output_path}")
            print(f"|001101|—|001101|—|111000|— data-spirit bound")
        
        # Update manifest
        target_locations = yaml_config.get('target_locations', [])
        target_paths = [loc.get('path', '') for loc in target_locations if isinstance(loc, dict)]
        
        if not args.dry_run:
            update_manifest(manifest_path, recipe_name, output_filename, target_paths, "✓ assembled")
    
    print(f"☠☠☠ >>> ASSEMBLY·PROTOCOL·COMPLETE ☠☠☠")
    print(f"Sacred recipe-relics processed: {len(recipe_files)} specimens")
    print(f"|001101|—|001101|—|111000|— communion terminated")
    return 0


if __name__ == "__main__":
    exit(main())