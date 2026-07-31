# Food Menu API

Production-ready FastAPI service for managing a food menu.

## Features

- Custom exceptions with structured error responses (`error_code`, `message`, `details`)
- Global exception handlers: app errors, HTTP errors, validation errors (422), and unhandled 500s
- Config via environment variables / `.env` (pydantic-settings)
- CORS middleware, request logging with timing, security headers
- Input validation on query/path params and models
- Health check endpoint (`/health`)
- Test suite (pytest)

## Run

```bash
uv sync
cp .env.example .env   # adjust as needed
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Development with auto-reload:

```bash
uv run uvicorn app.main:app --reload
```

## Test

```bash
uv run pytest
```

## Project layout

```
app/
  main.py        # FastAPI app, middleware, exception handlers, routes
  config.py      # Settings from env / .env
  exceptions.py  # Custom exception hierarchy
  models.py      # Pydantic schemas (request/response/error)
  data.py        # In-memory data store
tests/
  test_api.py
```

## Error response format

All errors follow a consistent shape:

```json
{
  "status": "error",
  "error_code": "item_not_found",
  "message": "Menu item with id 999 not found",
  "details": null
}
```

Validation failures include `details` with per-field errors.
