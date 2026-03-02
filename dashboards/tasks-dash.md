---
title: Tasks Dashboard
db: .system/db/tasks.db
---

# Tasks Dashboard

Source DB: `.system/db/tasks.db`  
Tables: `todos`, `edges`

## Status flow (locked)

Canonical `todos.status` lifecycle:
- `pending` → orchestrator trigger (unscheduled)
- `queued` → orchestrator scheduled into a bundle
- `running` → agent has begun work
- `completed` → agent finished work

Writer rules:
- Orchestrator sets `queued`.
- Agents set `running` and `completed` (and should not batch-complete at the end).

## Status totals

```sql
table: status_totals
columns: status, total
orderBy: total
orderDirection: desc
```
---
## Unbundled (not completed)

```sql
table: open_unbundled_todos
columns: id, status, summary, updated, bundle_id, spec_path
orderBy: updated
orderDirection: desc
```
## Missing pointers (`pointers_json == []`)

```sql
table: todos
columns: id, status, summary, updated, pointers_json, spec_path
filterColumn: pointers_json
filterValue: []
orderBy: updated
orderDirection: desc
```
---
## Pending (newest updated)

```sql
table: todos
columns: id, status, summary, updated, spec_path, bundle_id, thread_id, pointers_json, tags_json
filterColumn: status
filterValue: pending
orderBy: updated
orderDirection: desc
```
---
## Completed (most recently completed)

```sql
table: todos
columns: id, status, summary, completed_at, updated, spec_path, bundle_id
filterColumn: status
filterValue: completed
orderBy: completed_at
orderDirection: desc
```

## Operator vs Agent tasks

### Agent

```sql
table: todos
columns: id, status, summary, updated, spec_path, bundle_id
filterColumn: spec_origin
filterValue: agent
orderBy: updated
orderDirection: desc
```

### Operator

```sql
table: todos
columns: id, status, summary, updated, spec_path, bundle_id
filterColumn: spec_origin
filterValue: operator
orderBy: updated
orderDirection: desc
```
