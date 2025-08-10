import asyncio
from pathlib import Path
from typing import List, Union
from datetime import datetime

from config import OUTPUT_DIR, DEFAULT_TIMEOUT

async def run_command(command: Union[List[str], str], *, output_name: str, timeout: int = None, cwd: Path = None) -> tuple[str, str, int]:
    if timeout is None:
        timeout = DEFAULT_TIMEOUT

    if isinstance(command, list):
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
    else:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )

    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        process.kill()
        stdout, stderr = await process.communicate()
        returncode = -1
        print(f"O comando retornou TIMEOUT: {command}")
    else:
        returncode = process.returncode

    stdout_str = stdout.decode().strip()
    stderr_str = stderr.decode().strip()

    output_file_path = OUTPUT_DIR / f"{output_name}_output.log"
    with open(output_file_path, "a") as f:
        f.write(f"\n--- Command: {command} ---\n")
        f.write(f"--- Timestamp: {datetime.now().isoformat()} ---\n")
        if stdout_str:
            f.write(f"Stdout:\n{stdout_str}\n")
        if stderr_str:
            f.write(f"Stderr:\n{stderr_str}\n")
        f.write(f"Return Code: {returncode}\n")
        f.write(f"---\n")

    return stdout_str, stderr_str, returncode


