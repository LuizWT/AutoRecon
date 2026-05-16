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
    return f"  {Fore.CYAN}|{Fore.BLUE} {registry.info('nikto', mode)}{Fore.RESET}"


async def nikto_menu_loop(action: str = "run") -> None:
    mode_label = "Automação" if action == "queue" else "Execução"
    m = registry.REGISTRY["nikto"]["modes"]

    while True:
        clear_terminal()
        target = global_target.value
        target_display = (
            f"{Fore.GREEN}{target}{Fore.RESET}" if target
            else f"{Fore.RED}Não definido{Fore.RESET}"
        )

        print(rf"""
        {Fore.BLUE}
          _   _ _ _    _
         | \ | (_) |  | |      Ctrl+T → definir alvo
         |  \| |_| | _| |_ ___ Alvo: {target_display}{Fore.BLUE}
         | . ` | | |/ / __/ _ \Modo: {Fore.YELLOW}{mode_label}{Fore.BLUE}
         | |\  | |   <| || (_) |
         |_| \_|_|_|\_\\__\___/

        {Fore.CYAN}[1]{Fore.RESET} {m['vuln_checks']['label']}{_info('vuln_checks')}
        {Fore.CYAN}[2]{Fore.RESET} {m['server_modules']['label']}{_info('server_modules')}
        {Fore.CYAN}[3]{Fore.RESET} {m['config_files']['label']}{_info('config_files')}
        {Fore.CYAN}[4]{Fore.RESET} {m['cookie_security']['label']}{_info('cookie_security')}
        {Fore.CYAN}[5]{Fore.RESET} {m['protocols']['label']}{_info('protocols')}
        {Fore.CYAN}[6]{Fore.RESET} {m['dir_file_scan']['label']}{_info('dir_file_scan')}
        {Fore.CYAN}[7]{Fore.RESET} {m['third_party_scripts']['label']}{_info('third_party_scripts')}
        {Fore.CYAN}[8]{Fore.RESET} {m['all_commands']['label']}{_info('all_commands')}
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

        mode_map = {
            "1": "vuln_checks",
            "2": "server_modules",
            "3": "config_files",
            "4": "cookie_security",
            "5": "protocols",
            "6": "dir_file_scan",
            "7": "third_party_scripts",
        }

        if option in mode_map:
            mode = mode_map[option]
            await dispatch(action, "nikto", mode,
                           [registry.build("nikto", mode, target)])
        elif option == "8":
            if action == "run":
                confirm = await session.prompt_async(
                    HTML("<ansired>Executar 7 comandos em sequência? (y/n):</ansired> ")
                )
                if confirm.strip().lower() not in ("y", "s"):
                    continue
            await dispatch(action, "nikto", "all_commands",
                           registry.build_multi("nikto", "all_commands", target))
