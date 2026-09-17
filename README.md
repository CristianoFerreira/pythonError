# Python — Product API (FastAPI)

A minimal, in-memory Product CRUD API built with FastAPI.

## Prerequisites

- Python 3.11+

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --port 5005
```

The API listens on `http://localhost:5005`.

## Test

```bash
pytest
```

## API base URL

`http://localhost:5005`

## OpenAPI / Swagger

- OpenAPI JSON: `http://localhost:5005/openapi.json`
- Swagger UI: `http://localhost:5005/swagger`

Generated automatically by FastAPI from the route declarations and Pydantic models — no hand-written spec.

## Notes

- Storage is a single in-memory `dict[int, Product]` guarded by a `threading.Lock`, inside `ProductStore` (`app/store.py`), seeded with 2 sample products at startup.
- IDs are generated with a simple incrementing counter under the same lock.
- Validation (`name` required, `price >= 0`) is implemented with Pydantic `field_validator`s on `ProductRequest` (`app/models.py`). FastAPI's default response for invalid input is `422 Unprocessable Entity`; a custom exception handler in `app/main.py` converts this to `400 Bad Request` to match the shared contract.
- No SQLAlchemy, no dependency-injection containers, no repository layer — routes call the store directly.
