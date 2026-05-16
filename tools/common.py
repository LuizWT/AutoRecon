import asyncio
from colorama import Fore
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

from functions.runner import run_command
import tools.scheduler.queue as queue

_session = PromptSession()


async def dispatch(
    action: str,
    tool: str,
    mode: str,
    commands: list[list[str]],
) -> None:
    """
    Execute or enqueue a list of commands.

    action="run"   → runs each command immediately, streaming output to terminal.
    action="queue" → adds each command to the automation queue.
    """
    if action == "run":
        for cmd in commands:
            print(f"\n{Fore.CYAN}$ {' '.join(cmd)}{Fore.RESET}\n")
            _, stderr, rc = await run_command(cmd, output_name=tool, stream=True)
            if rc == 0:
                print(f"\n{Fore.GREEN}Concluído com sucesso.{Fore.RESET}")
            elif rc == -1:
                print(f"\n{Fore.YELLOW}Timeout: o comando foi encerrado.{Fore.RESET}")
            else:
                detail = stderr[:300] if stderr else "(sem saída de erro)"
                print(f"\n{Fore.RED}Erro (código {rc}): {detail}{Fore.RESET}")
        await _session.prompt_async(HTML("<ansiblue>\nPressione Enter para voltar...</ansiblue>"))
    else:
        for cmd in commands:
            queue.add(tool, mode, cmd)
        n = len(commands)
        label = "comando" if n == 1 else "comandos"
        print(f"\n{Fore.GREEN}[{n}] {label} adicionado(s) à fila.{Fore.RESET}")
        await asyncio.sleep(1.2)
