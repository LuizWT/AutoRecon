import json
from pathlib import Path
from colorama import Fore

_BASE = Path(__file__).resolve().parent
_QUEUE_DIR = _BASE / "storage"
_QUEUE_FILE = _QUEUE_DIR / "commands_queue.txt"


def _ensure() -> None:
    _QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    if not _QUEUE_FILE.exists():
        _QUEUE_FILE.write_text("")


def load() -> list[dict]:
    _ensure()
    lines = _QUEUE_FILE.read_text().strip().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def save(items: list[dict]) -> None:
    _ensure()
    with _QUEUE_FILE.open("w") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def add(tool: str, mode: str, command: list[str]) -> None:
    items = load()
    items.append({"tool": tool, "mode": mode, "command": command})
    save(items)


def remove(index: int) -> bool:
    items = load()
    if 0 <= index < len(items):
        items.pop(index)
        save(items)
        return True
    return False


def clear() -> None:
    save([])


def edit(index: int, new_command: list[str]) -> bool:
    items = load()
    if 0 <= index < len(items):
        items[index]["command"] = new_command
        save(items)
        return True
    return False


def apply_proxychains(index: int) -> tuple[bool, str]:
    items = load()
    if not (0 <= index < len(items)):
        return False, f"Índice {index + 1} inválido."
    cmd = items[index]["command"]
    if "proxychains" in cmd:
        return False, f"[{index + 1}] ProxyChains já aplicado."
    if cmd and cmd[0] == "sudo":
        new_cmd = ["sudo", "proxychains"] + cmd[1:]
    else:
        new_cmd = ["proxychains"] + cmd
    items[index]["command"] = new_cmd
    save(items)
    return True, f"[{index + 1}] {' '.join(cmd)}  →  {' '.join(new_cmd)}"


def format_list() -> list[str]:
    items = load()
    return [
        f"  {Fore.CYAN}[{i + 1}]{Fore.RESET} {' '.join(item['command'])}"
        for i, item in enumerate(items)
    ]
