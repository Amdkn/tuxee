Parent DOX: [adapter](../AGENTS.md).

# Purpose

Own the adapter smoke tests: constants, measured interface, doctor
all-pass, no network import in the adapter, describe.

# Ownership

Own `test_smoke.py`.

# Local Contracts

- Tests touch nothing upstream and make no network call; they run with
  the pas-B venv (`python -m pytest aspace-tuxee-adapter/tests/test_smoke.py -v`).

# Work Guidance

# Verification

`python -m pytest aspace-tuxee-adapter/tests/test_smoke.py -v` — 6 passed.

# Child DOX Index

No child DOX files.
