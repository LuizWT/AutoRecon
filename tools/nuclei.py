import asyncio
import os
from colorama import Fore, init
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

from functions.clear_terminal import clear_terminal
from functions.logger import get_logger
from functions.set_global_target import global_target, set_global_target
from functions.toggle_info import toggle_info, is_info_visible
from functions.validations.is_valid import is_valid_cidr
import tools.registry as registry
from tools.common import dispatch

init(autoreset=True)
session = PromptSession()
logger = get_logger(__name__)

_bindings = KeyBindings()


@_bindings.add("c-t")
def _(event):
    asyncio.create_task(set_global_target())


def _info(mode: str) -> str:
    if not is_info_visible():
        return ""
    return f"  {Fore.CYAN}|{Fore.BLUE} {registry.info('nuclei', mode)}{Fore.RESET}"


async def nuclei_menu_loop(action: str = "run") -> None:
    mode_label = "Automação" if action == "queue" else "Execução"
    m = registry.REGISTRY["nuclei"]["modes"]

    while True:
        clear_terminal()
        target = global_target.value
        target_display = (
            f"{Fore.GREEN}{target}{Fore.RESET}" if target
            else f"{Fore.RED}Não definido{Fore.RESET}"
        )

        print(rf"""
        {Fore.BLUE}
         _   _            _      _
        | \ | |          | |    (_)    Ctrl+T → definir alvo
        |  \| |_   _  ___| | ___ _    Alvo: {target_display}{Fore.BLUE}
        | . ` | | | |/ __| |/ _ \ |   Modo: {Fore.YELLOW}{mode_label}{Fore.BLUE}
        | |\  | |_| | (__| |  __/ |
        |_| \_|\__,_|\___|_|\___|_|

        {Fore.CYAN}[1]{Fore.RESET} {m['target_spec']['label']}{_info('target_spec')}
        {Fore.CYAN}[2]{Fore.RESET} {m['severity']['label']}{_info('severity')}
        {Fore.CYAN}[3]{Fore.RESET} {m['multi_target']['label']}{_info('multi_target')}
        {Fore.CYAN}[4]{Fore.RESET} {m['network_scan']['label']}{_info('network_scan')}
        {Fore.CYAN}[5]{Fore.RESET} {m['custom_template']['label']}{_info('custom_template')}
        {Fore.CYAN}[6]{Fore.RESET} {m['dashboard']['label']}{_info('dashboard')}
        {Fore.RED}[B]{Fore.RESET} Voltar   {Fore.YELLOW}[I]{Fore.RESET} Alternar Informações
        """)

        option = await session.prompt_async(
            HTML("<ansiyellow>Escolha:</ansiyellow> "), key_bindings=_bindings
        )
        option = option.strip()

        if option.lower() == "b":
            break
        if option.lower() == "i":
            toggle_info()
            continue

        target = global_target.value
        if not target and option not in ("3", "4"):
            logger.error("Nenhum alvo definido. Pressione Ctrl+T para configurar.")
            await session.prompt_async(HTML("<ansiblue>Enter para continuar...</ansiblue>"))
            continue

        if option == "1":
            await dispatch(action, "nuclei", "target_spec",
                           [registry.build("nuclei", "target_spec", target)])

        elif option == "2":
            while True:
                sev = await session.prompt_async(
                    HTML(
                        "<ansiyellow>Severidade (low, medium, high, critical)</ansiyellow>"
                        " <ansired>[B voltar]</ansired><ansiyellow>:</ansiyellow> "
                    )
                )
                if sev.strip().lower() == "b":
                    break
                if sev.strip().lower() in ("low", "medium", "high", "critical"):
                    await dispatch(action, "nuclei", "severity",
                                   [registry.build("nuclei", "severity", target,
                                                   severity=sev.strip().lower())])
                    break
                logger.error("Severidade inválida. Use: low, medium, high ou critical.")

        elif option == "3":
            while True:
                path = await session.prompt_async(
                    HTML(
                        "<ansiyellow>Caminho para o arquivo de alvos</ansiyellow>"
                        " <ansired>[B voltar]</ansired><ansiyellow>:</ansiyellow> "
                    )
                )
                if path.strip().lower() == "b":
                    break
                if os.path.isfile(path.strip()):
                    await dispatch(action, "nuclei", "multi_target",
                                   [registry.build("nuclei", "multi_target", path.strip())])
                    break
                logger.error(f"Arquivo não encontrado: {path.strip()}")

        elif option == "4":
            while True:
                cidr = await session.prompt_async(
                    HTML(
                        "<ansiyellow>Alvo de rede (ex: 192.168.1.0/24)</ansiyellow>"
                        " <ansired>[B voltar]</ansired><ansiyellow>:</ansiyellow> "
                    )
                )
                if cidr.strip().lower() == "b":
                    break
                if is_valid_cidr(cidr.strip()):
                    await dispatch(action, "nuclei", "network_scan",
                                   [registry.build("nuclei", "network_scan", cidr.strip())])
                    break
                logger.error("CIDR inválido.")

        elif option == "5":
            while True:
                raw = await session.prompt_async(
                    HTML(
                        "<ansiyellow>URL e caminho do template separados por espaço</ansiyellow>"
                        " <ansired>[B voltar]</ansired><ansiyellow>:</ansiyellow> "
                    )
                )
                if raw.strip().lower() == "b":
                    break
                parts = raw.strip().split(maxsplit=1)
                if len(parts) == 2:
                    await dispatch(action, "nuclei", "custom_template",
                                   [registry.build("nuclei", "custom_template",
                                                   parts[0], template=parts[1])])
                    break
                logger.error("Informe URL e template separados por espaço.")

        elif option == "6":
            await dispatch(action, "nuclei", "dashboard",
                           [registry.build("nuclei", "dashboard", target)])
