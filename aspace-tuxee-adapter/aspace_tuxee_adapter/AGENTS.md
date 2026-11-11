Parent DOX: [adapter](../AGENTS.md).

# Purpose

Own the `aspace_tuxee_adapter` package: `validate()`, `doctor()`,
`describe()` over the frozen tuxee tree.

# Ownership

Own `__init__.py` (the whole adapter).

# Local Contracts

- Standard library only; no network import, no network call, no write.
- Measurements are read from the repository tree at call time; constants
  (gel, bind, fiber address, Go module, Go version) are pinned in code.

# Work Guidance

# Verification

Smoke tests in `../tests/test_smoke.py` cover constants, the measured
interface, doctor all-pass, and the no-network-import check.

# Child DOX Index

No child DOX files.
