# Custom Project Steering

*Add custom steering modules to `.kiro/steering/` for project-specific context.*

## About Custom Steering

Kiro provides three default steering modules (product.md, structure.md, tech.md), but you can add any `.md` file to provide additional context:

- **api-patterns.md** - API design conventions and patterns
- **security.md** - Security requirements and best practices
- **deployment.md** - Deployment procedures and environments
- **testing.md** - Testing strategies and requirements
- **domain-model.md** - Business logic and domain relationships
- **{anything}.md** - Whatever context your project needs

**Naming matters**: The filename appears in Kiro's UI, so use descriptive names.

## What to Include

### Domain-Specific Patterns
- Business logic conventions
- Domain model relationships
- Workflow and process definitions
- Data validation rules

### Technical Constraints
- Performance requirements
- Security considerations
- Compliance requirements
- Browser/platform support matrix

### Team Conventions
- Code review guidelines
- Testing strategies
- Documentation standards
- Git workflow and branching

### Integration Points
- External service dependencies
- Third-party API usage patterns
- Database schema conventions
- Message queue patterns

## Example: api-patterns.md

```markdown
# API Patterns

## Authentication
- JWT tokens with refresh token rotation
- Access tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- All auth endpoints under `/api/auth/`

## Response Format
```json
{
  "data": { /* payload */ },
  "meta": { "timestamp": "ISO-8601" },
  "errors": [ /* if any */ ]
}
```

## Error Handling
- Use standard HTTP status codes
- Include error codes in response body
- Log all 5xx errors to monitoring
```

## Example: testing.md

```markdown
# Testing Strategy

## Requirements
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Minimum 80% code coverage for new code

## Conventions
- Test files: `*.test.ts` (unit), `*.integration.ts` (integration)
- Use `describe` blocks for grouping
- Use `it` for individual test cases
- Mock external dependencies in unit tests
```

## Tips

**Do:**
- Keep each file focused on one aspect
- Use concrete examples over abstract principles
- Update as project evolves
- Remove outdated content promptly

**Don't:**
- Duplicate content across files
- Include sensitive information (credentials, keys)
- Create files for temporary experiments
- Let steering drift from reality

---

*Create new `.md` files in `.kiro/steering/` as needed. Kiro loads them automatically.*

