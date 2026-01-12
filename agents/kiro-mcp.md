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