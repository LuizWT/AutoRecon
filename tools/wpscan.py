import asyncio
from colorama import Fore, init
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

from functions.clear_terminal import clear_terminal
from functions.logger import get_logger
from functions.set_global_target import global_target, set_global_target
from functions.toggle_info import toggle_info, is_info_visible
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
    return f"  {Fore.CYAN}|{Fore.BLUE} {registry.info('wpscan', mode)}{Fore.RESET}"


async def wpscan_menu_loop(action: str = "run") -> None:
    mode_label = "Automação" if action == "queue" else "Execução"
    m = registry.REGISTRY["wpscan"]["modes"]

    while True:
        clear_terminal()
        target = global_target.value
        target_display = (
            f"{Fore.GREEN}{target}{Fore.RESET}" if target
            else f"{Fore.RED}Não definido{Fore.RESET}"
        )

        print(rf"""
        {Fore.BLUE}
        __          _______   _____  _____          _   _
        \ \        / /  __ \ / ____|/ ____|   /\   | \ | |
         \ \  /\  / /| |__) | (___ | |       /  \  |  \| |
          \ \/  \/ / |  ___/ \___ \| |      / /\ \ | . ` |  Ctrl+T → alvo
           \  /\  /  | |     ____) | |____ / ____ \| |\  |  Alvo: {target_display}{Fore.BLUE}
            \/  \/   |_|    |_____/ \_____/_/    \_\_| \_|  Modo: {Fore.YELLOW}{mode_label}{Fore.BLUE}

        {Fore.CYAN}[1]{Fore.RESET} {m['normal']['label']}{_info('normal')}
        {Fore.CYAN}[2]{Fore.RESET} {m['enumerate_users']['label']}{_info('enumerate_users')}
        {Fore.CYAN}[3]{Fore.RESET} {m['enumerate_plugins']['label']}{_info('enumerate_plugins')}
        {Fore.CYAN}[4]{Fore.RESET} {m['enumerate_themes']['label']}{_info('enumerate_themes')}
        {Fore.CYAN}[5]{Fore.RESET} {m['scan']['label']}{_info('scan')}
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
        if not target:
            logger.error("Nenhum alvo definido. Pressione Ctrl+T para configurar.")
            await session.prompt_async(HTML("<ansiblue>Enter para continuar...</ansiblue>"))
            continue

        if option == "1":
            await dispatch(action, "wpscan", "normal",
                           [registry.build("wpscan", "normal", target)])
        elif option == "2":
            await dispatch(action, "wpscan", "enumerate_users",
                           [registry.build("wpscan", "enumerate_users", target)])
        elif option == "3":
            await dispatch(action, "wpscan", "enumerate_plugins",
                           [registry.build("wpscan", "enumerate_plugins", target)])
        elif option == "4":
            await dispatch(action, "wpscan", "enumerate_themes",
                           [registry.build("wpscan", "enumerate_themes", target)])
        elif option == "5":
            while True:
                token = await session.prompt_async(
                    HTML(
                        "<ansiyellow>API Token do WPScan</ansiyellow>"
                        " <ansired>[B voltar]</ansired><ansiyellow>:</ansiyellow> "
                    )
                )
                if token.strip().lower() == "b":
                    break
                if token.strip():
                    await dispatch(action, "wpscan", "scan",
                                   [registry.build("wpscan", "scan", target,
                                                   api_token=token.strip())])
                    break
                logger.error("API Token não pode ser vazio.")
