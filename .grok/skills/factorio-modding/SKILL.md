---
name: factorio-modding
description: Use when creating, editing, or debugging Factorio mods — writing prototypes
  in data.lua, handling events in control.lua, defining mod settings, structuring
  info.json, writing locale files, or diagnosing desync and prototype errors.
metadata:
  author: zk
  version: '1.0'
  category: gamedev
---

# Factorio Modding Reference

## Mod Directory Structure

```
mod-name_version.zip (distribution)
└── mod-name/
    ├── info.json          # required
    ├── data.lua           # prototype definitions
    ├── data-updates.lua   # modify other mods' prototypes
    ├── data-final-fixes.lua
    ├── settings.lua       # mod settings prototypes
    ├── settings-updates.lua
    ├── settings-final-fixes.lua
    ├── control.lua        # runtime scripting
    ├── migrations/        # save migration scripts
    └── locale/
        └── en/
            └── strings.cfg
```

Mod folder name = internal mod identifier. Files beyond the entry points must be loaded via `require()`.

---

## info.json Schema

```json
{
  "name": "mod-internal-name",
  "version": "1.0.0",
  "title": "Display Name",
  "author": "You",
  "factorio_version": "2.0",
  "description": "One line.",
  "dependencies": [
    "base >= 2.0",
    "? optional-mod",
    "! incompatible-mod"
  ]
}
```

Dependency prefixes: none = required, `?` = optional, `!` = incompatible.

---

## Load Order & Lifecycle

Mods load **by dependency depth, then alphabetically**. Three sequential stages at game startup:

### Stage 1 — Settings
`settings.lua` → `settings-updates.lua` → `settings-final-fixes.lua`  
Only `data` and `mods` tables available. No prototypes yet.

### Stage 2 — Data (prototype construction)
`data.lua` → `data-updates.lua` → `data-final-fixes.lua`  
`settings` variable available. No `game` object. Only `data:extend()` calls persist — all other Lua state is discarded.

Create prototypes in `data.lua` (earliest) so other mods can modify them downstream. Use `data-final-fixes.lua` to safely override after all mods have run.

### Stage 3 — Save Startup (per save load/create)
1. `control.lua` executes — register events, remote interfaces, commands. No `game` or `storage` yet.
2. `on_init()` — new saves only. Full `game` + `storage` access.
3. Migrations auto-run.
4. `on_load()` — existing saves. `storage` read-only. Only: metatable setup, conditional handlers, local references.
5. `on_configuration_changed()` — any config change. Full access.

---

## Prototype Patterns (data stage)

```lua
-- Deep copy from base
local myArmor = table.deepcopy(data.raw["armor"]["heavy-armor"])
myArmor.name = "fire-armor"
myArmor.resistances = { { type = "fire", decrease = 20, percent = 80 } }
data:extend{ myArmor }

-- From scratch
data:extend{{
  type = "recipe",
  name = "fire-armor",
  enabled = true,
  energy_required = 8,
  ingredients = {{ type = "item", name = "copper-plate", amount = 200 }},
  results = {{ type = "item", name = "fire-armor", amount = 1 }}
}}

-- Modify existing
data.raw["container"]["iron-chest"].max_health = 1000  -- in data-final-fixes.lua

-- Access pattern
data.raw["<prototype-type>"]["<internal-name>"]
```

In-game: `Shift+Ctrl+F` while hovering an item opens the prototype explorer (internal name + type).

---

## Event Handling (control stage)

```lua
-- control.lua
script.on_event(defines.events.on_player_changed_position, function(event)
  local player = game.get_player(event.player_index)
  if player.controller_type == defines.controllers.character then
    local inv = player.get_inventory(defines.inventory.character_armor)
    if inv.get_item_count("fire-armor") >= 1 then
      player.surface.create_entity{
        name = "fire-flame",
        position = player.position,
        force = "neutral"
      }
    end
  end
end)
```

Key namespaces: `defines.events.*`, `defines.controllers.*`, `defines.inventory.*`

---

## Global State — storage table

Use `storage` (not bare globals) for any state that must persist across save/load and stay synced in multiplayer.

```lua
script.on_init(function()
  storage.my_data = {}
end)

script.on_event(defines.events.on_something, function(event)
  storage.my_data[event.player_index] = true
end)
```

---

## Desync Prevention

Factorio is fully deterministic — all clients must produce identical state.

| Cause | Fix |
|---|---|
| Globals mutated outside event handlers | Use `storage` table |
| Conditional event subscription | Always subscribe at module top level |
| Table reference as key (`entity == other`) | Use `entity.unit_number` as key |
| `on_load` doing too much | Only: metatables, local refs, conditional handlers |

---

## Locale Format

`locale/en/strings.cfg` — INI-style, not Lua:

```cfg
[item-name]
fire-armor=Fire Armor

[item-description]
fire-armor=Burns the ground beneath you.

[mod-name]
fire-armor=Fire Armor Mod
```

Multiple languages: add `locale/de/`, `locale/fr/`, etc.

---

## Common Errors

| Error | Cause |
|---|---|
| `unfinished string near '...'` | Syntax error in data stage — check quotes/brackets |
| `attempt to index field '?' (a nil value)` | Wrong prototype type or name in `data.raw` |
| `Unknown entity name: foo` | Prototype not registered or typo in `name` field |
| Runtime error after save load | Syntax error in `control.lua` — doesn't prevent startup |
| Internal C++ crash | Engine bug — report with save + repro steps |

---

## Quick Reference

| What | Where | API |
|---|---|---|
| Define new item/entity/recipe | `data.lua` | `data:extend{}` |
| Modify base game prototypes | `data-final-fixes.lua` | `data.raw["type"]["name"].field = ...` |
| React to gameplay events | `control.lua` | `script.on_event(defines.events.X, fn)` |
| Persistent cross-session state | `control.lua` | `storage.key = value` |
| Add mod settings | `settings.lua` | `data:extend{{ type="bool-setting", ... }}` |
| Cross-mod API | `control.lua` | `remote.add_interface()` / `remote.call()` |
| Keyboard shortcuts | `control.lua` | `input.add_custom_input` + handler |

---

## API Docs

- Prototypes: `https://lua-api.factorio.com/latest/prototypes/`
- Runtime: `https://lua-api.factorio.com/latest/`
- Data lifecycle: `https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html`
- Mod structure: `https://lua-api.factorio.com/latest/auxiliary/mod-structure.html`
