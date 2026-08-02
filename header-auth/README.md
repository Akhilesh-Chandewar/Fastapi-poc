# Header Auth API

Production-ready FastAPI service demonstrating header-based API key authentication with `Users` and `Books` resources.

## Features

- **Header API-key auth**: every `/api/v1/*` route requires an `X-API-Key` header; validated with a constant-time comparison (`secrets.compare_digest`).
- **Full CRUD** for `Users` and `Books`, including search, filters, pagination, and a nested `GET /users/{id}/books` route.
- **Config via environment / `.env`** (`pydantic-settings`) — API key, database URL, CORS origins, app metadata.
- **Consistent, structured error responses** for HTTP errors, validation failures (422) and unexpected 500s.
- **CORS middleware + request logging** middleware with timing (`X-Process-Time-Ms` header).
- **Automatic table creation** on startup via the app `lifespan`.
- **Health check** (`/health`) and OpenAPI docs (`/docs`).
- **SQLModel** models with timezone-aware timestamps and validated inputs (`EmailStr`, price `>= 0`, lengths).

## Run

```bash
uv sync
cp .env.example .env   # set a strong API_KEY, adjust DATABASE_URL / CORS
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

Development with auto-reload:

```bash
uv run uvicorn main:app --reload
```

## Test

```bash
uv run pytest
```

## Auth

All API routes (except `/` and `/health`) require the API key:

```bash
curl -H "X-API-Key: <your-key>" http://localhost:8000/api/v1/users
```

## Routes

| Method | Path                        | Description                     |
| ------ | --------------------------- | ------------------------------- |
| GET    | `/health`                   | Health check                    |
| POST   | `/api/v1/users`             | Create a user                   |
| GET    | `/api/v1/users`             | List users (search/pagination)  |
| GET    | `/api/v1/users/{id}`        | Get a user                      |
| PUT    | `/api/v1/users/{id}`        | Update a user                   |
| DELETE | `/api/v1/users/{id}`        | Delete a user                   |
| GET    | `/api/v1/users/{id}/books`  | List books owned by a user      |
| POST   | `/api/v1/books`             | Create a book                   |
| GET    | `/api/v1/books`             | List books (filter/pagination)  |
| GET    | `/api/v1/books/{id}`        | Get a book                      |
| PUT    | `/api/v1/books/{id}`        | Update a book                   |
| DELETE | `/api/v1/books/{id}`        | Delete a book                   |

## Error response format

```json
{
  "status": "error",
  "error_code": "http_error",
  "message": "User not found"
}
```

Validation failures include an array of per-field `details`.