# Update Copilot Instructions

Use this prompt to keep .github/copilot-instructions.md current.

## Quick Review Prompt

Ask Copilot:
```
Review .github/copilot-instructions.md against the current codebase.

Check for:
1. Code patterns in use that aren't documented
2. Documented patterns that have changed
3. New enums, types, or constants not listed
4. New environment variables not documented
5. New make commands not listed
6. Any SQLAlchemy/Pydantic reserved name conflicts discovered

Output a summary of suggested updates in this format:

## Suggested Updates

### Section: [name]
- **Change**: [add/modify/remove]
- **Content**: [what to add/change]
- **Reason**: [why]
```

## After Major Changes

Run this check after:
- Adding new database models or enums
- Creating new API endpoints with novel patterns
- Adding new environment variables
- Updating the Makefile
- Discovering new reserved name conflicts
- Changing project structure

## Update Frequency

- **Weekly**: Quick review during team sync
- **After features**: Check if new patterns emerged
- **After bugs**: Check if a conflict should be documented
