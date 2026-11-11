Parent DOX: [project](../AGENTS.md).

# Purpose

Own the A'Space adapter for tuxee (`fiber:a0:tuxee`): a read-only contract
that observes the frozen tuxee provisioning/usage interface (install.sh,
compose.yaml, Dockerfile, cmd/tuxee, docker/) and documents how the stack
(agent-zero + spynel + a0-plugins) provisions on tuxee, without adapting
the framework or the chat, and without touching the OS code (D10).

# Ownership

Own `aspace_tuxee_adapter/` (validate / doctor / describe) and `tests/`
(adapter smoke tests). Root owns the DOX index row that registers this
directory. The adapter never modifies upstream files.

# Local Contracts

- The adapter is Python, standard library only: no network import, no
  network call, no write, no upstream file modified.
- The adapter never provisions anything itself; it reads the frozen tree
  and reports measurements. Installation downloads the official GitHub
  release (sha256 verified) and requires root on Linux.
- Use the exact tagline `Tuxee - the most convenient Linux for servers and agents.` when naming the product.
- This directory is A'Space-owned adapter scope inside the sovereign fork
  `Amdkn/tuxee` (D-N053 pas B); the upstream remains byte-identical to
  the gel except for the one-line DOX index entry in the root AGENTS.md
  that registers this directory (DOX-required, see the adaptation sheet).

# Work Guidance

Run the smoke tests with the pas-B venv:
`python -m pytest aspace-tuxee-adapter/tests/test_smoke.py -v`.

# Verification

Smoke: constants, measured interface, doctor all-pass, no network import
in the adapter (AST-checked), describe. The upstream suite is
`go test ./...` with `TUXEE_SYSTEM_TEST=1` (see the adaptation sheet).

# Child DOX Index

- [aspace_tuxee_adapter/AGENTS.md](aspace_tuxee_adapter/AGENTS.md): Adapter package (validate / doctor / describe).
- [tests/AGENTS.md](tests/AGENTS.md): Adapter smoke tests.
