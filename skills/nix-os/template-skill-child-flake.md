
```nix
{
  description = "Agent Skills Catalog";

  inputs = {
    # Pin your skills source here
    anthropic-skills.url = "github:anthropics/skills";
    anthropic-skills.flake = false;
    
    # You can add more sources
    # my-skills.url = "path:./my-skills";
    # my-skills.flake = false;
  };

  outputs = { self, anthropic-skills, ... }: {
    homeManagerModules.default = { config, lib, ... }: {
      programs.agent-skills = {
        
        # Define where skills come from
        sources.anthropic = {
          path = anthropic-skills;
          subdir = "skills";
        };

        # Declaratively enable specific skills
        skills.enable = [ 
          "frontend-design" 
          "skill-creator" 
        ];

        # Or enable everything from a source
        # skills.enableAll = [ "anthropic" ];
      };
    };
  };
}
```