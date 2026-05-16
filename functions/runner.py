import asyncio
from pathlib import Path
from typing import Union
from datetime import datetime

from config import OUTPUT_DIR, DEFAULT_TIMEOUT
from functions.logger import get_logger

logger = get_logger(__name__)


async def run_command(
    command: Union[list[str], str],
    *,
    output_name: str,
    timeout: int = None,
    cwd: Path = None,
    stream: bool = False,
) -> tuple[str, str, int]:
    """
    Run a command and capture its output.

    Pass a list[str] for safe exec (no shell injection risk).
    Pass a str only for install scripts that genuinely require shell features (&&, $(), etc).

    stream=True prints stdout live to the terminal as the process runs.
    All output is always saved to output/<output_name>_output.log.
    """
    if timeout is None:
        timeout = DEFAULT_TIMEOUT

    if isinstance(command, list):
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )
    else:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

    stdout_parts: list[str] = []
    stderr_parts: list[str] = []

    async def _read(pipe: asyncio.StreamReader, parts: list[str], do_stream: bool) -> None:
        while True:
            chunk = await pipe.read(4096)
            if not chunk:
                break
            text = chunk.decode(errors="replace")
            parts.append(text)
            if do_stream:
                print(text, end="", flush=True)

    returncode = -1
    try:
        async with asyncio.timeout(timeout):
            await asyncio.gather(
                _read(process.stdout, stdout_parts, stream),
                _read(process.stderr, stderr_parts, False),
            )
            await process.wait()
            returncode = process.returncode
    except TimeoutError:
        process.kill()
        await process.wait()
        logger.warning(f"Timeout ao executar: {command}")

    stdout_str = "".join(stdout_parts)
    stderr_str = "".join(stderr_parts).strip()

    output_file = OUTPUT_DIR / f"{output_name}_output.log"
    with open(output_file, "a") as f:
        f.write(f"\n--- Command: {command} ---\n")
        f.write(f"--- Timestamp: {datetime.now().isoformat()} ---\n")
        if stdout_str.strip():
            f.write(f"Stdout:\n{stdout_str}\n")
        if stderr_str:
            f.write(f"Stderr:\n{stderr_str}\n")
        f.write(f"Return Code: {returncode}\n---\n")

    return stdout_str, stderr_str, returncode
