from pathlib import Path

import yaml

from functions.proxy_chains import ProxyManager

_DEFS_DIR = Path(__file__).parent / "definitions"


def _load_registry() -> dict:
    result = {}
    for path in sorted(_DEFS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        result[data["name"]] = data
    return result


REGISTRY: dict[str, dict] = _load_registry()


def _wrap(cmd: list[str], sudo: bool) -> list[str]:
    if not sudo:
        return cmd
    if ProxyManager.is_enabled():
        return ["sudo", "proxychains"] + cmd
    return ["sudo"] + cmd


def _render(template: list[str], **kwargs) -> list[str]:
    return [elem.format(**kwargs) for elem in template]


def build(tool: str, mode: str, target: str, **kwargs) -> list[str]:
    """Returns a single command as a list of args (safe for create_subprocess_exec)."""
    mode_def = REGISTRY[tool]["modes"][mode]
    sudo = REGISTRY[tool].get("sudo", False)
    for param, spec in mode_def.get("params", {}).items():
        if param not in kwargs and "default" in spec:
            kwargs[param] = spec["default"]
    return _wrap(_render(mode_def["command"], target=target, **kwargs), sudo)


def build_multi(tool: str, mode: str, target: str, **kwargs) -> list[list[str]]:
    """Returns a list of commands for multi-step modes."""
    mode_def = REGISTRY[tool]["modes"][mode]
    sudo = REGISTRY[tool].get("sudo", False)
    return [_wrap(_render(t, target=target, **kwargs), sudo) for t in mode_def["commands"]]


def is_multi(tool: str, mode: str) -> bool:
    return REGISTRY[tool]["modes"][mode].get("multi", False)


def info(tool: str, mode: str) -> str:
    return REGISTRY[tool]["modes"][mode].get("info", "")
