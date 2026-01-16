## Workspace Steering

Kiro
- `C:\Users\synta.ZK-ZRRH\.dev\.kiro\steering\compiled-workspace.md`

All Agents
- `C:\Users\synta.ZK-ZRRH\.dev\AGENTS.md`

## Multi-Workspace Navigation
- **Path Parameter**: Use `executePwsh(path="workspace_root")` to specify which workspace to run commands from
- **Absolute Paths in Scripts**: In multi-workspace setups, hardcode absolute paths in scripts rather than relying on relative paths
- **Workspace Roots**: 
  - `z:\Documents\.context` - Context/documentation workspace
  - `c:\Users\synta.ZK-ZRRH\.dev` - Development workspace  
  - `\\wsl.localhost\Ubuntu-22.04\home\zk\.wsl-dev` - WSL workspace

### Script Execution Pattern
```python
# In Python scripts, use absolute paths for cross-workspace access
base_path = Path("Z:/Documents/.context")  # Context workspace root
script_path = Path("C:/Users/synta.ZK-ZRRH/.dev/.scripts")  # Scripts location
```

### Common Pitfall

- Running executePwsh(command="python script.py", path="workspace_a") but script looks for files relative to workspace_a
- **Solution**: Hardcode absolute paths in the script itself, not relative to execution 
