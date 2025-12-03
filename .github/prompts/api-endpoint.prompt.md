# Create API Endpoint

Create a new FastAPI endpoint in apps/api/src/routers/

## Requirements

- Router file: `{router_name}.py`
- Endpoint: `{method} {path}`
- Description: {description}

## Template

Follow this structure:

1. Create router with prefix and tags
2. Import dependencies (Depends, HTTPException, Session)
3. Import schemas from src/schemas/
4. Import service from src/services/
5. Use dependency injection for database session: `db: Session = Depends(get_db)`
6. Return appropriate status codes (200, 201, 404, etc.)
7. Add response_model for type safety

## Watch Out For
- Always use Depends(get_db) for database sessions
- Use HTTPException for errors, not bare raises
- Add tags for OpenAPI documentation
- Include docstrings for complex endpoints
