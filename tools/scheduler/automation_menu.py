import asyncio
import sys
from colorama import Fore, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

from functions.clear_terminal import clear_terminal
from functions.set_global_target import global_target
from functions.runner import run_command
from functions.logger import get_logger
from configurations.ar_updater import new_version_checker
from configurations.version import __version__
import tools.scheduler.queue as queue

from tools.nmap import nmap_menu_loop
from tools.sniper import sniper_menu_loop
from tools.wpscan import wpscan_menu_loop
from tools.nuclei import nuclei_menu_loop
from tools.nikto import nikto_menu_loop

init(autoreset=True)
session = PromptSession()
logger = get_logger(__name__)


async def _execute_commands_in_intervals(interval_minutes: int) -> None:
    stop = asyncio.Event()

    async def _wait_for_enter() -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, sys.stdin.readline)
        stop.set()

    print(
        f"{Fore.CYAN}Automação iniciada com intervalo de {interval_minutes} minuto(s)."
        f"\n{Fore.YELLOW}Pressione Enter para interromper.{Fore.RESET}\n"
    )

    enter_task = asyncio.create_task(_wait_for_enter())
    iteration = 0

    try:
        while not stop.is_set():
            iteration += 1
            items = queue.load()
            if not items:
                print(f"{Fore.YELLOW}Fila vazia. Automação encerrada.{Fore.RESET}")
                break

            print(f"{Fore.CYAN}[Iteração {iteration}] Executando {len(items)} comando(s)...{Fore.RESET}")
            for item in items:
                if stop.is_set():
                    break
                cmd = item["command"]
                tool = item.get("tool", "custom")
                logger.info(f"Executando: {' '.join(cmd)}")
                await run_command(cmd, output_name=tool)

            if stop.is_set():
                break

            print(
                f"\n{Fore.GREEN}[Iteração {iteration}] Concluída."
                f" Próxima em {interval_minutes}m. Enter para parar.{Fore.RESET}\n"
            )

            sleep_task = asyncio.create_task(asyncio.sleep(interval_minutes * 60))
            done, _ = await asyncio.wait(
                {enter_task, sleep_task}, return_when=asyncio.FIRST_COMPLETED
            )
            if enter_task in done:
                sleep_task.cancel()
                break
            enter_task = asyncio.create_task(_wait_for_enter())

    except asyncio.CancelledError:
        pass
    finally:
        enter_task.cancel()
        print(f"\n{Fore.GREEN}Automação encerrada após {iteration} iteração(ões).{Fore.RESET}")


async def _queue_editor() -> None:
    while True:
        clear_terminal()
        items = queue.load()
        formatted = queue.format_list()

        print(f"\n{Fore.BLUE}{Style.BRIGHT}=== Fila de Automação ==={Style.RESET_ALL}")
        if formatted:
            print("\n".join(formatted))
        else:
            print(f"  {Fore.YELLOW}(fila vazia){Fore.RESET}")

        has_items = bool(items)
        print(f"\n  {Fore.CYAN}[A]{Fore.RESET} Adicionar comando customizado")
        if has_items:
            print(
                f"  {Fore.CYAN}[E]{Fore.RESET} Editar comando\n"
                f"  {Fore.CYAN}[P]{Fore.RESET} Aplicar ProxyChains\n"
                f"  {Fore.RED}[R]{Fore.RESET} Remover comando\n"
                f"  {Fore.RED}[RA]{Fore.RESET} Remover todos"
            )
        print(f"  {Fore.RED}[B]{Fore.RESET} Voltar\n")

        choice = (await session.prompt_async(HTML("<ansiyellow>Escolha:</ansiyellow> "))).strip().lower()

        if choice == "b":
            return

        elif choice == "a":
            raw = await session.prompt_async(HTML("<ansiyellow>Comando customizado:</ansiyellow> "))
            cmd = raw.strip().split()
            if cmd:
                queue.add("custom", "custom", cmd)
                print(f"{Fore.GREEN}Adicionado: {' '.join(cmd)}{Fore.RESET}")
                await asyncio.sleep(1)

        elif choice == "r" and has_items:
            idx_str = await session.prompt_async(HTML("<ansiyellow>Índice para remover:</ansiyellow> "))
            try:
                if queue.remove(int(idx_str.strip()) - 1):
                    print(f"{Fore.GREEN}Removido.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Índice inválido.{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}Entrada inválida.{Fore.RESET}")
            await asyncio.sleep(1)

        elif choice == "ra" and has_items:
            confirm = await session.prompt_async(
                HTML("<ansiyellow>Remover todos os comandos? (y/n):</ansiyellow> ")
            )
            if confirm.strip().lower() in ("y", "s"):
                queue.clear()
                print(f"{Fore.GREEN}Fila limpa.{Fore.RESET}")
                await asyncio.sleep(1)

        elif choice == "e" and has_items:
            idx_str = await session.prompt_async(HTML("<ansiyellow>Índice para editar:</ansiyellow> "))
            try:
                idx = int(idx_str.strip()) - 1
                current_items = queue.load()
                if 0 <= idx < len(current_items):
                    old_cmd = " ".join(current_items[idx]["command"])
                    new_raw = await session.prompt_async(
                        HTML("<ansiyellow>Novo comando:</ansiyellow> "), default=old_cmd
                    )
                    new_cmd = new_raw.strip().split()
                    if new_cmd:
                        queue.edit(idx, new_cmd)
                        print(f"{Fore.GREEN}Atualizado.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Índice inválido.{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}Entrada inválida.{Fore.RESET}")
            await asyncio.sleep(1)

        elif choice == "p" and has_items:
            idx_str = await session.prompt_async(
                HTML("<ansiyellow>Índice(s) para ProxyChains (ex: 1,3):</ansiyellow> ")
            )
            try:
                indices = [int(x.strip()) - 1 for x in idx_str.split(",")]
                for idx in indices:
                    ok, msg = queue.apply_proxychains(idx)
                    color = Fore.GREEN if ok else Fore.YELLOW
                    print(f"{color}{msg}{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}Entrada inválida.{Fore.RESET}")
            await asyncio.sleep(1.5)


_TOOL_MENUS = {
    "1": sniper_menu_loop,
    "2": nmap_menu_loop,
    "3": wpscan_menu_loop,
    "4": nuclei_menu_loop,
    "5": nikto_menu_loop,
}


async def automation_setup_menu() -> None:
    while True:
        clear_terminal()
        is_outdated = new_version_checker()
        update_msg = (
            f"{Fore.RED}Desatualizado — use 'sudo autorecon --update'{Fore.RESET}"
            if is_outdated
            else f"{Fore.GREEN}Atualizado{Fore.RESET}"
        )
        target_display = (
            f"{Fore.GREEN}{global_target.value}{Fore.RESET}"
            if global_target.value
            else f"{Fore.RED}Não definido{Fore.RESET}"
        )
        queue_count = len(queue.load())
        queue_display = (
            f"{Fore.GREEN}{queue_count} comando(s){Fore.RESET}"
            if queue_count
            else f"{Fore.YELLOW}vazia{Fore.RESET}"
        )

        print(rf"""
{Fore.BLUE}{Style.BRIGHT}
   _____     _____      _              _       _
  |  _  |   /  ___|    | |            | |     | |
  | | | |   \ `--.  ___| |__   ___  __| |_   _| | ___ _ __
  | | | |    `--. \/ __| '_ \ / _ \/ _` | | | | |/ _ \ '__|
  | |_| /   /\__/ / (__| | | |  __/ (_| | |_| | |  __/ |
  \_____/    \____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|
{Style.RESET_ALL}
{Fore.YELLOW}+ -- --=[ AutoRecon {__version__} | {update_msg}
{Fore.YELLOW}+ -- --=[ Alvo: {target_display}   Fila: {queue_display}

  {Fore.YELLOW}Adicionar à fila:{Style.RESET_ALL}
  {Fore.CYAN}[1]{Fore.RESET} SNIPER      {Fore.CYAN}[2]{Fore.RESET} NMAP
  {Fore.CYAN}[3]{Fore.RESET} WPSCAN      {Fore.CYAN}[4]{Fore.RESET} NUCLEI
  {Fore.CYAN}[5]{Fore.RESET} NIKTO

  {Fore.CYAN}[A]{Fore.RESET} Iniciar Automação   {Fore.CYAN}[Q]{Fore.RESET} Editar Fila
  {Fore.RED}[B]{Fore.RESET} Voltar
        """)

        choice = (await session.prompt_async(HTML("\n<ansiyellow>Escolha:</ansiyellow> "))).strip()

        if choice in _TOOL_MENUS:
            clear_terminal()
            await _TOOL_MENUS[choice](action="queue")

        elif choice.lower() == "a":
            if not queue.load():
                logger.error("A fila está vazia. Adicione comandos antes de iniciar.")
                await asyncio.sleep(2)
                continue

            interval_str = await session.prompt_async(
                HTML("<ansiyellow>Intervalo em minutos</ansiyellow> <ansired>[B voltar]</ansired><ansiyellow>:</ansiyellow> ")
            )
            if interval_str.strip().lower() == "b":
                continue
            try:
                interval = int(interval_str.strip())
                if interval <= 0:
                    raise ValueError
            except ValueError:
                logger.error("Intervalo inválido. Insira um número inteiro positivo.")
                await asyncio.sleep(2)
                continue

            clear_terminal()
            await _execute_commands_in_intervals(interval)
            await session.prompt_async(HTML("<ansiblue>Pressione Enter para continuar...</ansiblue>"))

        elif choice.lower() == "q":
            await _queue_editor()

        elif choice.lower() == "b":
            clear_terminal()
            return
