import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import yaml

from functions.runner import run_command
from tools import registry

_PROFILES_DIR = Path(__file__).parent.parent / "profiles"


@dataclass
class StepResult:
    tool: str
    mode: str
    label: str
    command: list[str]
    stdout: str
    stderr: str
    returncode: int
    started_at: datetime
    finished_at: datetime

    @property
    def duration(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    @property
    def success(self) -> bool:
        return self.returncode == 0


@dataclass
class ScanResult:
    target: str
    profile: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    steps: list[StepResult] = field(default_factory=list)

    @property
    def duration(self) -> float:
        if self.finished_at is None:
            return 0.0
        return (self.finished_at - self.started_at).total_seconds()


def load_profile(name: str) -> dict:
    path = _PROFILES_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Perfil não encontrado: {name}")
    return yaml.safe_load(path.read_text())


def list_profiles() -> list[dict]:
    profiles = []
    for path in sorted(_PROFILES_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        profiles.append({
            "name": data["name"],
            "label": data["label"],
            "description": data.get("description", ""),
            "steps": len(data.get("steps", [])),
        })
    return profiles


async def run_scan(
    target: str,
    profile_name: str,
    *,
    stream: bool = True,
    on_step_start: Optional[Callable[[dict], None]] = None,
    on_step_done: Optional[Callable[[StepResult], None]] = None,
) -> ScanResult:
    profile = load_profile(profile_name)
    result = ScanResult(
        target=target,
        profile=profile_name,
        started_at=datetime.now(),
    )

    for step in profile.get("steps", []):
        tool = step["tool"]
        mode = step["mode"]
        label = step.get("label", f"{tool}/{mode}")

        if registry.is_multi(tool, mode):
            commands = registry.build_multi(tool, mode, target)
        else:
            commands = [registry.build(tool, mode, target)]

        if on_step_start:
            on_step_start({"tool": tool, "mode": mode, "label": label})

        for cmd in commands:
            started = datetime.now()
            stdout, stderr, rc = await run_command(
                cmd,
                output_name=f"scan_{profile_name}_{tool}",
                stream=stream,
            )
            finished = datetime.now()
            step_result = StepResult(
                tool=tool,
                mode=mode,
                label=label,
                command=cmd,
                stdout=stdout,
                stderr=stderr,
                returncode=rc,
                started_at=started,
                finished_at=finished,
            )
            result.steps.append(step_result)
            if on_step_done:
                on_step_done(step_result)

    result.finished_at = datetime.now()
    return result
