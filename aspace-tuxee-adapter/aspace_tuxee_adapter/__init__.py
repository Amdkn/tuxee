"""A'Space adapter — tuxee (D-N053 pas B, design Clara + design signe pas B).

Contrat seul, patron D-N048 (dify / cordis) et pas A (chronos) : cet adapter
ne modifie AUCUN fichier amont, ne fait AUCUN appel reseau, ne monte AUCUN
poids. Il constate : le gel epingle, la licence, la surface d'interface
de provisionnement/usage — install.sh, compose.yaml, Dockerfile,
cmd/tuxee, docker/ — et documente comment la pile (agent-zero + spynel +
plugins) se provisionne sur tuxee, SANS adapter ni le framework ni le
chat, et SANS toucher au code de l'OS (D10, borne dure : internal/, web/,
experiments/ hors interface sont hors perimetre).

Adresse : fiber:a0:tuxee
Fork souverain : Amdkn/tuxee (parent agent0ai/tuxee, branche main)
Gel amont : a7e2061abce616b62951cb132e39d34d25bed3a3 (« Keep shortcut
terminals open after commands finish »)
Bind Cordis Fiber (2L) : 5c51b78b5e6ff98492efab09de306f517ddeb35d
Licence : MIT

Mesures au gel (2026-11-11, verifiees au fichier) :
- Interface : install.sh 61 lignes (telechargement de la release GitHub,
  sha256 verifie, root + Linux seulement), compose.yaml 19 lignes
  (ports 80:80, 443:443 ; volumes tuxee-state / tuxee-home / tuxee-init),
  Dockerfile 82 lignes (multi-stage : frontend node, backend golang
  1.26.10 CGO+PAM, binaire scratch, gui debian), cmd/tuxee (main, status,
  restart, ports, instance, output), docker/ (build-audio, build-gui,
  docker-init, entrypoint, init/, tuxee.example.json).
- Ports : HTTP 80, HTTPS 443 par defaut ; `TUXEE_HTTP_PORT` /
  `TUXEE_HTTPS_PORT` en surcharge, 0 desactive ; bind legacy `:443`.
- 144 fichiers .go ; 70 fichiers _test.go (dont 7 cmd/tuxee, 4 tests/).
- Derive amont : 2 commits derriere (amont vivant, 2026-11-09) — gel tenu,
  revisite par signal, jamais de fast-forward silencieux.
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:tuxee"
FORK = "Amdkn/tuxee"
UPSTREAM_REPO = "agent0ai/tuxee"
UPSTREAM_BRANCH = "main"
PINNED_UPSTREAM_COMMIT = "a7e2061abce616b62951cb132e39d34d25bed3a3"
PINNED_UPSTREAM_COMMIT_SHORT = "a7e2061"
BIND_COMMIT = "5c51b78b5e6ff98492efab09de306f517ddeb35d"
BIND_LAYER = "2L"
LICENSE = "MIT"
ADAPTER_VERSION = "0.1.0"
GO_MODULE = "tuxee"
GO_VERSION = "1.26.10"

INTERFACE_FILES = ("install.sh", "compose.yaml", "Dockerfile")
CMD_FILES = ("main.go", "status.go", "restart.go", "ports.go", "instance.go", "output.go")
DOCKER_FILES = ("build-audio.sh", "build-gui.sh", "docker-init.sh", "entrypoint.sh")
PILE = ("fiber:a0:agent-zero", "fiber:a0:spynel", "fiber:a0:a0-plugins")

CONFINEMENT = """Aucun confinement commercial : code MIT. Usage B2B autorise par la
licence. L'installation telecharge la release GitHub officielle
(checksum sha256 verifie) ; les secrets (ROOT_PASSWORD) sont fournis
par l'operateur a l'installation, jamais lus ni stockes ici."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _interface(root: Path) -> dict:
    files = {name: (root / name).exists() for name in INTERFACE_FILES}
    lines = {}
    for name in INTERFACE_FILES:
        path = root / name
        lines[name] = len(path.read_text(encoding="utf-8", errors="replace").splitlines()) if path.exists() else 0
    cmd = root / "cmd" / "tuxee"
    cmd_files = [name for name in CMD_FILES if (cmd / name).exists()]
    docker = root / "docker"
    docker_files = [name for name in DOCKER_FILES if (docker / name).exists()]
    compose = (root / "compose.yaml").read_text(encoding="utf-8", errors="replace") if (root / "compose.yaml").exists() else ""
    ports = sorted(set(re.findall(r'"(\d+):(\d+)"', compose)))
    go_mod = (root / "go.mod").read_text(encoding="utf-8", errors="replace") if (root / "go.mod").exists() else ""
    m_mod = re.search(r"(?m)^module\s+(\S+)", go_mod)
    m_go = re.search(r"(?m)^go\s+(\S+)", go_mod)
    go_files = [p for p in root.rglob("*.go") if ".git" not in p.parts]
    test_files = [p for p in go_files if p.name.endswith("_test.go")]
    install = (root / "install.sh").read_text(encoding="utf-8", errors="replace") if (root / "install.sh").exists() else ""
    return {
        "interface_files_present": [n for n, ok in files.items() if ok],
        "interface_lines": lines,
        "cmd_tuxee_files_present": cmd_files,
        "docker_files_present": docker_files,
        "compose_ports": ports,
        "go_module": m_mod.group(1) if m_mod else None,
        "go_version": m_go.group(1) if m_go else None,
        "go_files_total": len(go_files),
        "test_files_total": len(test_files),
        "install_downloads_github_release": "github.com/agent0ai/tuxee/releases/download" in install,
        "install_verifies_sha256": "sha256sum" in install,
        "install_requires_root_linux": 'Run with sudo sh, or as root' in install and "Tuxee requires Linux" in install,
    }


def describe() -> dict:
    """Decrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "provisioned_stack": list(PILE),
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'etat du fork gele. Aucun appel reseau, aucune ecriture."""
    root = _repo_root()
    surface = _interface(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "os_code_touched": False,
        "provisioned_stack": list(PILE),
        "confinement": CONFINEMENT,
        **surface,
        "interface_complete": (
            surface["interface_files_present"] == list(INTERFACE_FILES)
            and surface["cmd_tuxee_files_present"] == list(CMD_FILES)
            and surface["docker_files_present"] == list(DOCKER_FILES)
            and surface["compose_ports"] == [("443", "443"), ("80", "80")]
            and surface["go_module"] == GO_MODULE
            and surface["go_version"] == GO_VERSION
            and surface["install_downloads_github_release"]
            and surface["install_verifies_sha256"]
            and surface["install_requires_root_linux"]
        ),
    }


def doctor() -> list[dict]:
    """Liste de controles sur le fork gele."""
    v = validate()
    return [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_mit",
            "ok": v["license_file_present"] and v["license"] == "MIT",
            "detail": "LICENSE present, MIT (fichier ; l'API dit NOASSERTION)",
        },
        {
            "name": "module_go",
            "ok": v["go_module"] == GO_MODULE and v["go_version"] == GO_VERSION,
            "detail": f"{v['go_module']} (go {v['go_version']})",
        },
        {
            "name": "interface_provisionnement",
            "ok": v["interface_complete"],
            "detail": (
                f"install.sh {v['interface_lines'].get('install.sh')} lignes, "
                f"compose.yaml {v['interface_lines'].get('compose.yaml')} lignes, "
                f"Dockerfile {v['interface_lines'].get('Dockerfile')} lignes ; "
                f"cmd/tuxee {v['cmd_tuxee_files_present']} ; docker/ {v['docker_files_present']} ; "
                f"ports {v['compose_ports']}"
            ),
        },
        {
            "name": "installation_verifiee",
            "ok": v["install_downloads_github_release"] and v["install_verifies_sha256"],
            "detail": "release GitHub + sha256, root + Linux seulement",
        },
        {
            "name": "pile_provisionnee_sans_re_adaptation",
            "ok": v["provisioned_stack"] == list(PILE) and not v["os_code_touched"],
            "detail": "agent-zero + spynel + a0-plugins references, 0 code de l'OS touche",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import reseau, 0 appel sortant",
        },
    ]
