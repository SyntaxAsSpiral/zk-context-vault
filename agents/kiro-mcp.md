---
id: kiro-mcp
title: "Kiro MCP Integration"
type: 
  - "documentation"
  - "configuration"
category: "agents"
tags:
  - "kiro"
  - "mcp"
  - "model-context-protocol"
  - "servers"
  - "integration"
created: 2026-01-11
modified: 2026-01-11
status: "active"
glyph: "🔌"
lens: "external-integration"
---

# 🔌 Kiro MCP Integration

*Model Context Protocol server configurations for external tool access.*

## kiro-sdk-task-db

location(s):
- `C:\Users\synta.ZK-ZRRH\.dev\amexsomnemon\.kiro\settings\mcp.json`

```
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {},
      "disabled": true,
      "autoApprove": []
    },
    "tasks": {
      "type": "stdio",
      "command": "node",
      "args": [
        ".system/node/mcp-servers/tasks/index.mjs"
      ],
      "env": {}
    }
  }
}
```