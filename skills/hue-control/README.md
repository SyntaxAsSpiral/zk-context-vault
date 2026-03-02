# Hue Control Skill

Integration reference for Philips Hue smart lighting via CLI (not MCP).

## Approach: CLI Wrapper

Preferred pattern (matching x-research-skill): a lightweight CLI that wraps the Hue v2 API, callable via Bash from agents.

### Hue API v2 (CLIP)

- Local bridge API: `https://{bridge-ip}/clip/v2`
- Auth: Application Key (generated via bridge button press)
- Discovery: mDNS or https://discovery.meethue.com
- Full OpenAPI spec: [openhue/openhue-api](https://github.com/openhue/openhue-api)

### Existing CLI Tools

- **[openhue-cli](https://github.com/openhue/openhue-cli)** — Go CLI for Hue v2 API
  - `openhue get lights`, `openhue set light <id> --on --brightness 80`
  - Could install in container directly
- **[phue](https://github.com/studioimaginaire/phue)** — Python library
- **[hue-control](https://github.com/tigoe/hue-control)** — Educational reference

### MCP Alternatives (if needed for workshop deployment)

- [rmrfslashbin/hue-mcp](https://github.com/rmrfslashbin/hue-mcp) — Node.js MCP server
- [ThomasRohde/hue-mcp](https://github.com/ThomasRohde/hue-mcp) — Another implementation
- Multiple on LobeHub MCP marketplace

## Setup Requirements

1. **Hue Bridge IP** — discover via `https://discovery.meethue.com` or mDNS
2. **Application Key** — press bridge button, then POST to `https://{bridge-ip}/api` with `{"devicetype":"nanoclaw#adeck"}`
3. **Env vars**: `HUE_BRIDGE_IP`, `HUE_APP_KEY`

## NanoClaw Integration Path

1. Build a `hue-ctl` CLI (Bun/Node/Go) or use openhue-cli
2. Install in container image
3. Pass bridge IP + app key via env mount
4. SKILL.md teaches agent the CLI commands
5. Network: container needs access to local bridge IP (Docker `--network host` or bridge network with route to LAN)

## Consideration: Network Access

Hue bridge is on LAN. Docker containers are isolated by default. Options:
- `--network host` (simplest, least isolated)
- Bridge network with LAN route
- Proxy on host that forwards to bridge
