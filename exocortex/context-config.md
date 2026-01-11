---
id: context-config
created: 2026-01-01T15:23:47.603-08:00
modified: 2026-01-01T21:52:08.221-08:00
status: locked
---
# Model Presets and Config

```yaml

agents:
  archeoform:
    llm:
      backend: default
      model: default
      preset: default
    enabled: true
    max_concurrency: 1

  harmonion:
    llm:
      backend: default
      model: default
      preset: default
    enabled: true
    max_concurrency: 1   

  morphognome:
    llm:
      backend: default
      model: default
      preset: default
    enabled: true
    max_concurrency: 1

  critikon:
    llm:
      backend: default
      model: default
      preset: default
    enabled: true
    max_concurrency: 1

  antimorphogen:
    llm:
      backend: default
      model: default
      preset: default
    enabled: true
    max_concurrency: 1

llm:
  # Defaults to LM Studio for development (free/local).
  default:
    backend: lmstudio
    model: openai/gpt-oss-20b
    preset: default

  # Backends are OpenAI-compatible chat completion endpoints.
  backends:
    lmstudio:
      base_url: http://localhost:1234/v1
      api_key_env: LMSTUDIO_API_KEY
    openrouter:
      base_url: https://openrouter.ai/api/v1
      api_key_env: OPENROUTER_API_KEY
      title: system
      referer: ""
    pollinations:
      base_url: https://text.pollinations.ai/openai
      api_key_env: POLLINATIONS_API_KEY

  presets:
    default:
      temperature: 1.0
    balanced:
      temperature: 0.4
      top_p: 1.0
      max_tokens: 30000
    precise:
      temperature: 0.2
      top_p: 1.0
      max_tokens: 30000

semantic:
  # Auxiliary semantic index for scalable dossier compilation (non-authoritative).
  # Stored in SQLite; can point at the graph DB if you want a single file.
  backend: lmstudio
  model: text-embedding-nomic-embed-text-v1.5
  batch_size: 64
  index_db_path: TODO<add .system/ path>

```