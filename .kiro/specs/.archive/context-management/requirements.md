# Requirements Document

## Introduction

A context management system for IDE integration that assembles sliced markdown content using YAML recipes and provides minimal tasks for execution. The system uses the existing organized context library structure and outputs assembled content to `workshop/staging/` with recipes in `workshop/` for configuration.

## Glossary

- **Context_Library**: The `.context/` directory containing organized source documentation
- **Recipe**: YAML configuration embedded in markdown that specifies assembly instructions
- **Slice**: Marked sections in context files using HTML comment markers (`<!-- slice:id -->`) for granular extraction
- **Whole_File_Source**: A source that includes an entire file without slice extraction
- **Assembly_Task**: IDE task that processes a recipe to generate assembled output
- **Export_Task**: IDE task that copies assembled content from output folder to target locations
- **Workshop**: The `workshop/` directory containing recipes and staging
- **Staging_Folder**: The `workshop/staging/` directory for assembled content
- **Multi_Section_Recipe**: A recipe with multiple output sections separated by `---` markers
- **Template**: Optional string with `{content}` placeholder for custom output formatting
- **Output_Format**: Specifies folder structure (skill = Agent Skills standard, power = POWER.md + steering/)
- **Skill_Structure**: Agent Skills standard with SKILL.md (frontmatter + body) at root, optional scripts/, references/, assets/ subfolders
- **Power_Structure**: Folder with POWER.md at root, optional mcp.json, and steering/ subfolder for guides
- **Source_Role**: Grouped sources (power_md, mcp_config, steering_files, skill_md, scripts, references, assets) that map to specific output locations
- **Agent_Skills_Standard**: Format specification from agentskills.io defining SKILL.md frontmatter requirements and folder structure

## Requirements

### Requirement 1: Recipe-Based Configuration

**User Story:** As a developer, I want YAML recipes embedded in markdown that specify how to assemble context content, so that I can configure different outputs for agents, skills, and powers with varying complexity.

#### Acceptance Criteria

1. WHEN creating recipes, THE Recipe_System SHALL support YAML embedded in markdown format with Obsidian frontmatter
2. WHEN defining assembly instructions, THE Recipe SHALL specify sources (slices or whole files) and target output locations
3. WHEN configuring for different systems, THE Recipe SHALL support agent, skill, power, and custom recipe types
4. WHEN simple assembly is needed, THE Recipe MAY omit the template field and use direct concatenation
5. WHEN complex assembly is needed, THE Recipe MAY include type-specific fields (agent_format, skill_type, power_structure, etc.)
6. WHEN multiple outputs are needed from one recipe, THE Recipe MAY use `---` separators to define multiple output sections
7. THE Recipe_System SHALL store all recipes in the `workshop/` directory

### Requirement 2: Flexible Source Assembly

**User Story:** As a developer, I want to assemble content from both sliced sections and whole files, so that I can create targeted outputs with granular control for complex cases and simple inclusion for straightforward cases.

#### Acceptance Criteria

1. WHEN a source specifies `slice` + `slice-file`, THE Assembly_Engine SHALL extract content between slice markers from the specified file
2. WHEN a source specifies only `file`, THE Assembly_Engine SHALL include the entire file content
3. WHEN assembling content, THE Assembly_Engine SHALL combine multiple sources in the order specified by the recipe
4. WHEN a template is provided, THE Assembly_Engine SHALL substitute `{content}` with the assembled content
5. WHEN no template is provided, THE Assembly_Engine SHALL use the assembled content directly
6. THE Assembly_Engine SHALL output all assembled content to `workshop/staging/`

### Requirement 3: Minimal IDE Task Integration

**User Story:** As a developer, I want minimal IDE tasks for assembly and export operations, so that I can execute context management workflows efficiently.

#### Acceptance Criteria

1. WHEN executing the assembly task, THE Assembly_Task SHALL process all valid recipes in the workshop directory
2. WHEN executing the sync task, THE Sync_Task SHALL sync all valid content from the output folder to target locations
3. WHEN syncing content, THE Sync_Task SHALL delete files at target locations that were previously synced but are no longer in output
4. WHEN tasks execute, THE Task_System SHALL provide clear feedback on success or failure
5. THE Task_System SHALL follow the semantic JSON plugin command style for consistency

### Requirement 4: Output Logging and Versioning

**User Story:** As a developer, I want current version outputs logged to the workshop output folder, so that I can track and validate assembled content.

#### Acceptance Criteria

1. WHEN assembly completes, THE Output_Logger SHALL save assembled content to `workshop/staging/`
2. WHEN generating outputs, THE Output_Logger SHALL include version information and timestamps
3. WHEN content changes, THE Output_Logger SHALL maintain previous versions for comparison
4. WHEN validating outputs, THE Output_Logger SHALL provide copies for manual review
5. THE Output_Logger SHALL organize outputs by recipe type and target system

### Requirement 5: Agent Recipe Processing

**User Story:** As a developer, I want agent recipes that assemble persona and behavioral content with minimal configuration, so that I can generate consistent agent definitions for different AI systems.

#### Acceptance Criteria

1. WHEN processing agent recipes, THE Agent_Processor SHALL support simple source lists without templates for basic agents
2. WHEN assembling agent content, THE Agent_Processor SHALL concatenate sources with double newlines by default
3. WHEN agent recipes include templates, THE Agent_Processor SHALL apply template substitution for custom formatting
4. WHEN agent recipes specify multiple output sections, THE Agent_Processor SHALL create separate outputs per section
5. WHEN agent recipes include agent_format field, THE Agent_Processor SHALL validate output format matches target system
6. THE Agent_Processor SHALL support Claude, Kiro, OpenAI, and custom agent formats

### Requirement 6: Skill Recipe Processing

**User Story:** As a developer, I want skill recipes that create Agent Skills standard folder structures with SKILL.md (frontmatter + body), optional scripts/, references/, and assets/ folders, so that I can deploy skills across multiple platforms following the agentskills.io specification.

#### Acceptance Criteria

1. WHEN output_format is "skill", THE Skill_Processor SHALL create folder structure following Agent Skills standard (SKILL.md + optional scripts/, references/, assets/)
2. WHEN skill_md source is specified, THE Skill_Processor SHALL generate SKILL.md with required YAML frontmatter (name, description) and markdown body
3. WHEN scripts are specified, THE Skill_Processor SHALL write executable files to scripts/ subfolder
4. WHEN references are specified, THE Skill_Processor SHALL write documentation files to references/ subfolder
5. WHEN assets are specified, THE Skill_Processor SHALL write static resources to assets/ subfolder
6. WHEN validate_agentskills_spec is true, THE Skill_Processor SHALL validate name format (lowercase, numbers, hyphens only, max 64 chars) and description (max 1024 chars)
7. WHEN also_output_as_power is true, THE Skill_Processor SHALL generate both Agent Skills and Kiro Power folder structures
8. WHEN multiple target_locations are specified, THE Skill_Processor SHALL deploy to all locations (e.g., Kiro, Claude)

### Requirement 7: Power Recipe Processing

**User Story:** As a developer, I want power recipes that create structured folders with POWER.md at root and steering files in steering/ subfolder, so that I can package complete Kiro powers.

#### Acceptance Criteria

1. WHEN output_format is "power", THE Power_Processor SHALL create folder structure with POWER.md at root and steering/ subfolder
2. WHEN power_md source is specified, THE Power_Processor SHALL assemble content and write to POWER.md at root
3. WHEN mcp_config source is specified, THE Power_Processor SHALL write mcp.json to root (optional)
4. WHEN steering_files are specified, THE Power_Processor SHALL write each file to steering/ subfolder with specified output_name
5. WHEN metadata is provided, THE Power_Processor SHALL include version, author, description, keywords, and category in POWER.md frontmatter
6. THE Power_Processor SHALL ensure all steering files are .md format (JSON/HTML embedded in markdown)

### Requirement 8: Export and Synchronization

**User Story:** As a developer, I want a single sync task that manages all target locations, so that I can deploy all assembled content with one command.

#### Acceptance Criteria

1. WHEN executing the sync task, THE Sync_System SHALL process all valid content in the workshop staging folder
2. WHEN syncing content, THE Sync_System SHALL copy content to all target locations specified in recipes
3. WHEN files exist at target locations but are no longer in staging, THE Sync_System SHALL delete them
4. WHEN target locations don't exist, THE Sync_System SHALL create directory structures as needed
5. THE Sync_System SHALL maintain a sync manifest to track what was previously deployed for cleanup

### Requirement 9: Recipe Validation and Testing

**User Story:** As a developer, I want validation of recipes and assembled outputs, so that I can catch errors before deployment.

#### Acceptance Criteria

1. WHEN validating recipes, THE Validator SHALL check YAML syntax and required fields
2. WHEN checking slice references, THE Validator SHALL verify that all referenced slices exist
3. WHEN validating outputs, THE Validator SHALL compare assembled content against expected formats
4. WHEN running tests, THE Validator SHALL execute dry-run assembly operations
5. THE Validator SHALL provide clear error messages and suggestions for fixes

### Requirement 10: Workshop Organization and Management

**User Story:** As a developer, I want organized workshop structure for recipes and outputs, so that I can maintain clean separation between configuration and generated content.

#### Acceptance Criteria

1. WHEN organizing recipes, THE Workshop_Manager SHALL store all recipes in `workshop/`
2. WHEN generating outputs, THE Workshop_Manager SHALL organize content in `workshop/staging/` by type
3. WHEN managing versions, THE Workshop_Manager SHALL maintain clean separation between current and historical outputs
4. WHEN cleaning up, THE Workshop_Manager SHALL provide tasks to remove stale outputs
5. THE Workshop_Manager SHALL maintain consistent directory structure and naming conventions

### Requirement 11: Absolute Path Configuration

**User Story:** As a developer, I want all scripts to use absolute paths for workspace directories, so that they work consistently regardless of execution context in the multi-workspace environment.

#### Acceptance Criteria

1. WHEN scripts initialize, THE Script_System SHALL use absolute paths for all workspace directories
2. WHEN resolving context library paths, THE Script_System SHALL use `Z:\Documents\.context` as the absolute base path
3. WHEN resolving script paths, THE Script_System SHALL use `C:\Users\synta.ZK-ZRRH\.dev\.scripts` as the absolute scripts directory
4. WHEN processing file references in recipes, THE Script_System SHALL resolve all paths relative to the absolute context base path
5. THE Script_System SHALL not rely on current working directory for path resolution

### Requirement 12: Multi-Section Recipe Support

**User Story:** As a developer, I want to define multiple outputs in a single recipe file using section separators, so that I can organize related outputs together (like Kiro's agent, operator, and principles files).

#### Acceptance Criteria

1. WHEN a recipe contains `---` separators between YAML blocks, THE Assembly_Engine SHALL treat each section as a separate output specification
2. WHEN processing multi-section recipes, THE Assembly_Engine SHALL generate one output file per section
3. WHEN naming outputs from multi-section recipes, THE Assembly_Engine SHALL use the target path filename or a section-specific name
4. WHEN sections share the same recipe name, THE Assembly_Engine SHALL append section identifiers to output filenames
5. THE Assembly_Engine SHALL process all sections in a single recipe file during one assembly run

### Requirement 13: Structured Output Formats

**User Story:** As a developer, I want recipes to specify output_format (skill or power) to automatically create proper folder structures, so that assembled content follows platform conventions (Agent Skills standard and Kiro Power format).

#### Acceptance Criteria

1. WHEN output_format is "skill", THE Assembly_Engine SHALL create Agent Skills standard structure (SKILL.md with frontmatter at root, optional scripts/, references/, assets/ subfolders)
2. WHEN output_format is "power", THE Assembly_Engine SHALL create Kiro Power structure (POWER.md at root, optional mcp.json, steering/ subfolder)
3. WHEN sources specify output_name, THE Assembly_Engine SHALL use that name for the output file
4. WHEN sources are grouped by role (power_md, mcp_config, steering_files, skill_md, scripts, references, assets), THE Assembly_Engine SHALL place files in appropriate locations
5. WHEN also_output_as_power is true in skill recipes, THE Assembly_Engine SHALL generate both Agent Skills and Kiro Power folder structures
6. WHEN validate_agentskills_spec is true, THE Assembly_Engine SHALL validate skill name format and description length per agentskills.io specification
7. THE Assembly_Engine SHALL ensure power steering files are .md format and skill SKILL.md has required frontmatter fields