"""Root pytest conftest for the vnstock-advisor app.

The shared Settings schema (vnstock_shared.config) requires JWT keys with no
defaults, and there is no committed .env (gitignored). Supply dev/test-only
placeholder values so every service suite can collect and run in a clean
checkout — CI executes `pytest -q` at app root. These placeholders are NOT
production secrets; real deployments must inject real keys via env vars.
"""

import os

os.environ.setdefault("JWT_PRIVATE_KEY", "dev-private-key-change-in-production")
os.environ.setdefault("JWT_PUBLIC_KEY", "dev-public-key-change-in-production")
