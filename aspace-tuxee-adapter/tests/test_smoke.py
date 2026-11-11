"""Smoke tests de l'adapter tuxee (D-N053 pas B).

Roules avec le venv du pas : `python -m pytest aspace-tuxee-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel reseau.
"""

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_tuxee_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:tuxee"
    assert adapter.LICENSE == "MIT"
    assert adapter.FORK == "Amdkn/tuxee"
    assert adapter.UPSTREAM_REPO == "agent0ai/tuxee"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "5c51b78b5e6ff98492efab09de306f517ddeb35d"
    assert adapter.GO_MODULE == "tuxee"
    assert adapter.GO_VERSION == "1.26.10"


def test_validate_interface():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["interface_files_present"] == ["install.sh", "compose.yaml", "Dockerfile"]
    assert v["interface_lines"] == {"install.sh": 61, "compose.yaml": 19, "Dockerfile": 82}
    assert v["cmd_tuxee_files_present"] == ["main.go", "status.go", "restart.go", "ports.go", "instance.go", "output.go"]
    assert v["docker_files_present"] == ["build-audio.sh", "build-gui.sh", "docker-init.sh", "entrypoint.sh"]
    assert v["compose_ports"] == [("443", "443"), ("80", "80")]
    assert v["go_module"] == "tuxee"
    assert v["go_version"] == "1.26.10"
    assert v["go_files_total"] == 144
    assert v["test_files_total"] == 70
    assert v["install_downloads_github_release"] is True
    assert v["install_verifies_sha256"] is True
    assert v["install_requires_root_linux"] is True
    assert v["os_code_touched"] is False
    assert v["interface_complete"] is True
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_provisioned_stack():
    v = adapter.validate()
    assert v["provisioned_stack"] == ["fiber:a0:agent-zero", "fiber:a0:spynel", "fiber:a0:a0-plugins"]


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    tree = ast.parse(src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp", "http"):
        assert banned not in imported, banned
    assert imported <= {"re", "pathlib", "__future__", "annotations"}, imported


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:tuxee"
    assert d["provisioned_stack"] == ["fiber:a0:agent-zero", "fiber:a0:spynel", "fiber:a0:a0-plugins"]
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "MIT"
