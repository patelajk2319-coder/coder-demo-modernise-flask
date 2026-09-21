# coder-demo-modernise-flask

A deliberately old-style Flask API — the "before" side of a Flask → FastAPI
modernization demo. Paired with
[coder-template-modernise-agent](https://github.com/patelajk2319-coder/coder-template-modernise-agent),
which provisions a network-locked, audit-logged Coder workspace for interactively
upgrading this app with Claude Code while keeping its API surface identical.

## What's deliberately legacy here

- `app.run(host="0.0.0.0", port=8000, debug=True)` — the Werkzeug dev server, not a
  production entrypoint.
- No type hints anywhere.
- `GET /items/<item_id>` casts `item_id` to `int()` manually and aborts 404 on a miss,
  instead of a `<int:item_id>` route converter.
- `POST /items` validates the request body by hand (`if "name" not in body`) instead
  of a schema/model.
- A single in-memory list (`ITEMS`), loaded once at import and rewritten to
  `data.json` on every write — no locking, no database, no concurrency safety.
- `Flask==2.2.5` / `Werkzeug==2.2.3` — old enough to predate typed, auto-documented
  frameworks like FastAPI.

None of this is a trick or a landmine — it's meant to be a small, honest legacy
codebase, not a puzzle.

## API contract to preserve

This is the definition of done for a modernization: `tests/test_app.py` asserts the
exact status codes and response shapes below. Porting these same assertions into a
FastAPI `TestClient` test file — same expected bodies/codes, different client
boilerplate — is how you prove the rewrite kept the surface identical.

| Method | Path | Response |
|---|---|---|
| `GET` | `/items` | `200`, JSON array of `{id, name, quantity}` |
| `GET` | `/items/<id>` | `200` + the item, or `404` if not found |
| `POST` | `/items` | `201` + the created item (`{name, quantity}` required in the body) |

## Local development

```bash
pip install -r requirements-dev.txt
task test    # run the test suite
task run     # Flask dev server on :8000
task build   # Docker build + run on :8000
```

## Branching

Modernization work happens on `modernize/<coder-workspace-name>` branches, created
automatically by the Coder workspace template — never on `main`. `main` has GitHub
branch protection (no direct pushes, PR + review required) as a backstop.
