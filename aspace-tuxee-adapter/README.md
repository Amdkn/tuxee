# A'Space adapter — tuxee

**Adresse :** `fiber:a0:tuxee` — D-N053 pas B (design Clara, design signé pas B D-B0..D-B3).
**Fork souverain :** `Amdkn/tuxee` (parent `agent0ai/tuxee`, branche `main`).
**Gel amont :** `a7e2061abce616b62951cb132e39d34d25bed3a3` (« Keep shortcut terminals open after commands finish »).
**Bind Cordis Fiber (2L) :** `5c51b78b5e6ff98492efab09de306f517ddeb35d` — `aspace-plugin.json`, re-appliqué VERBATIM sur `main` au-dessus de l'adapter (F8 D2).
**Licence :** `MIT`.
**Version adapter :** 0.1.0 — contrat seul, patron D-N048 (dify / cordis) et pas A (chronos).

## Ce que fait l'adapter

Tuxee — the most convenient Linux for servers and agents. L'adapter est
un adapter **d'interface** (D10, borne dure) : il documente comment la
pile Agent Zero se provisionne sur tuxee et constate la surface
d'interface — `install.sh` (release GitHub, sha256 vérifié, root +
Linux seulement), `compose.yaml` (ports 80/443, volumes
tuxee-state / tuxee-home / tuxee-init), `Dockerfile` (multi-stage :
frontend node, backend golang 1.26.10 CGO+PAM, binaire scratch, gui
debian), `cmd/tuxee` (main, status, restart, ports, instance, output),
`docker/` (build-audio, build-gui, docker-init, entrypoint, init/).
La pile provisionnée : `fiber:a0:agent-zero` + `fiber:a0:spynel` +
`fiber:a0:a0-plugins` — référencée, jamais ré-adaptée. **Jamais le code
de l'OS** (`internal/`, `web/`, `experiments/` hors interface).

Surface : `validate()` (constate : gel, licence, module Go, interface
mesurée au fichier, zéro appel réseau), `doctor()` (liste de
contrôles), `describe()` (manifeste machine). **Aucun fichier amont
touché** (hors la ligne d'index DOX requise par le contrat du repo, voir
la fiche), **aucun appel réseau, aucun poids monté dans le fork.**

Mesures au gel : 144 fichiers `.go`, 70 fichiers `_test.go` ; dérive
amont 2 (gel tenu, revisite par signal).

## Confinement

Aucun confinement commercial : code MIT. Usage B2B autorisé par la
licence. L'installation télécharge la release GitHub officielle
(checksum sha256 vérifié) ; les secrets (`ROOT_PASSWORD`) sont fournis
par l'opérateur à l'installation, jamais lus ni stockés ici.

## Tests

```bash
python -m pytest aspace-tuxee-adapter/tests/test_smoke.py -v
```

Smoke : constantes (gel 40-hex, adresse fiber, pile provisionnée,
licence, module Go), `validate()` vert (interface complète mesurée),
`doctor()` tout ok, zéro import réseau dans l'adapter. La suite amont
est celle du module au gel (`go test ./...` avec `TUXEE_SYSTEM_TEST=1`,
voir la fiche d'adaptation : `tuxee-ADAPTATION.md`, évidence
D-N053/b/tuxee/).
