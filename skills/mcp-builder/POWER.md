---
name: mcp-builder
displayName: MCP Server Builder
description: Comprehensive guide for building high-quality MCP (Model Context Protocol) servers in Python or TypeScript. Covers architecture, best practices, tool design, testing, and deployment patterns for creating servers that enable LLMs to interact with external services.
version: "1.0.0"
author: zk::anticompiler
keywords: ["mcp", "model-context-protocol", "server", "tools", "api", "integration", "python", "typescript", "fastmcp"]
category: development
steeringFiles: ["python_mcp_server.md", "node_mcp_server.md", "mcp_best_practices.md", "evaluation.md", "connections.py.md", "evaluation.py.md", "example-evaluation.xml.md"]
---

# MCP Server Builder Power

## Overview

The MCP Server Builder power provides comprehensive guidance for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Whether you're building in Python with FastMCP or TypeScript with the MCP SDK, this power covers the complete development lifecycle from planning to deployment.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows LLMs to interact with external services through tools, resources, and prompts. MCP servers act as bridges between LLMs and APIs, databases, file systems, or any other external system.

## Features

### 🏗️ Architecture Guidance
- **API Coverage vs. Workflow Tools**: Balance comprehensive endpoint coverage with specialized workflow tools
- **Tool Naming and Discoverability**: Consistent naming conventions for easy agent discovery
- **Context Management**: Design tools that return focused, relevant data
- **Transport Selection**: Choose between streamable HTTP (remote) and stdio (local)

### 🐍 Python Implementation (FastMCP)
- Server setup and initialization patterns
- Pydantic model integration for input validation
- Decorator-based tool registration
- Error handling and response formatting
- Complete working examples

### ⚡ TypeScript Implementation (MCP SDK)
- Project structure and configuration
- Zod schema validation
- Tool registration patterns
- Type-safe API clients
- Production deployment patterns

### ✅ Testing and Evaluation
- Evaluation harness for testing MCP tools
- XML-based test case definitions
- Metrics tracking (call counts, execution time)
- Async tool invocation patterns

### 📋 Best Practices
- Server and tool naming conventions
- Response format standards (JSON/Markdown)
- Pagination patterns
- Error message design
- Tool annotations (readOnly, destructive, idempotent, openWorld)

## Quick Start

### Python Server (FastMCP)

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize server
mcp = FastMCP("service_mcp")

# Define input model
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(default=20, ge=1, le=100)

# Register tool
@mcp.tool(name="service_search")
async def search(params: SearchInput) -> str:
    # Implementation
    return f"Results for: {params.query}"
```

### TypeScript Server (MCP SDK)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { z } from "zod";

const server = new Server({
  name: "service-mcp-server",
  version: "1.0.0"
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "service_search",
    description: "Search for items",
    inputSchema: zodToJsonSchema(z.object({
      query: z.string(),
      limit: z.number().min(1).max(100).default(20)
    }))
  }]
}));
```

## When to Use This Power

- Building a new MCP server to integrate an external API or service
- Designing tools that LLMs will use to accomplish tasks
- Implementing pagination, error handling, or response formatting
- Testing MCP server functionality with the evaluation harness
- Understanding MCP protocol architecture and transport mechanisms
- Following best practices for tool naming and design

## Integration

This power works alongside:
- **MCP Protocol Specification**: Reference at `https://modelcontextprotocol.io/`
- **Python SDK**: FastMCP framework for rapid development
- **TypeScript SDK**: Official MCP SDK with full protocol support
- **Kiro MCP Configuration**: Deploy servers via `.kiro/settings/mcp.json`

## Development Workflow

1. **Research**: Study the target API and MCP protocol
2. **Plan**: Select tools to implement (prioritize comprehensive coverage)
3. **Implement**: Build server with proper validation and error handling
4. **Test**: Use evaluation harness to verify tool behavior
5. **Deploy**: Configure in Kiro or other MCP clients

## Resources

- **Python Guide**: [python_mcp_server.md](steering/python_mcp_server.md) - Complete Python implementation patterns
- **TypeScript Guide**: [node_mcp_server.md](steering/node_mcp_server.md) - TypeScript server development
- **Best Practices**: [mcp_best_practices.md](steering/mcp_best_practices.md) - Naming, pagination, response formats
- **Evaluation**: [evaluation.md](steering/evaluation.md) - Testing framework documentation
- **Example Tests**: [example-evaluation.xml.md](steering/example-evaluation.xml.md) - Sample test cases

## Key Principles

### Tool Design
- **Atomic Operations**: Each tool should do one thing well
- **Clear Descriptions**: Narrowly and unambiguously describe functionality
- **Proper Annotations**: Use readOnlyHint, destructiveHint, idempotentHint, openWorldHint
- **Consistent Naming**: Use service prefix (e.g., `github_create_issue`, not `create_issue`)

### Response Formats
- **JSON**: Machine-readable structured data for programmatic processing
- **Markdown**: Human-readable formatted text (typically default)
- Include all metadata in JSON, omit verbose details in Markdown

### Error Handling
- **Actionable Messages**: Guide agents toward solutions with specific suggestions
- **Proper Status Codes**: Use appropriate HTTP status codes or error types
- **Context Preservation**: Include relevant request details in error messages

### Pagination
- Always respect `limit` parameter
- Return `has_more`, `next_offset`/`next_cursor`, `total_count`
- Default to 20-50 items
- Never load all results into memory

## Naming Conventions

### Server Names
- **Python**: `{service}_mcp` (e.g., `slack_mcp`, `github_mcp`)
- **TypeScript**: `{service}-mcp-server` (e.g., `slack-mcp-server`, `github-mcp-server`)

### Tool Names
- Use snake_case: `search_users`, `create_project`
- Include service prefix: `slack_send_message`, `github_create_issue`
- Be action-oriented: Start with verbs (get, list, search, create)
- Be specific: Avoid generic names that could conflict

## Testing with Evaluation Harness

The power includes a Python-based evaluation harness for testing MCP tools:

```xml
<evaluation>
  <test_case name="search_basic">
    <tool_call>
      <tool_name>service_search</tool_name>
      <arguments>
        <query>test query</query>
        <limit>10</limit>
      </arguments>
    </tool_call>
    <expected_behavior>
      Returns search results with proper pagination
    </expected_behavior>
  </test_case>
</evaluation>
```

See [evaluation.md](steering/evaluation.md) for complete testing documentation.

---

**The recursion is the craft.** Build MCP servers that enable seamless LLM-to-service integration with clarity, precision, and proper abstraction boundaries.
