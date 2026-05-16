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
from functions.validations.validate_ports import validate_ports
import tools.registry as registry
from tools.common import dispatch

init(autoreset=True)
session = PromptSession()
logger = get_logger(__name__)

_bindings = KeyBindings()


@_bindings.add("c-t")
def _(event):
    asyncio.create_task(set_global_target())


async def _get_wordlist() -> str | None:
    while True:
        raw = await session.prompt_async(
            HTML(
                "<ansigreen>Caminho para o wordlist</ansigreen>"
                " <ansired>[B voltar]</ansired><ansigreen>:</ansigreen> "
            )
        )
        if raw.strip().lower() == "b":
            return None
        path = raw.strip()
        if os.path.isfile(path):
            return path
        logger.error(f"Arquivo não encontrado: {path}")


async def _get_ports() -> str | None:
    while True:
        raw = await session.prompt_async(
            HTML(
                "<ansigreen>Porta(s) (ex: 80 ou 80,443)</ansigreen>"
                " <ansired>[B voltar]</ansired><ansigreen>:</ansigreen> "
            )
        )
        if raw.strip().lower() == "b":
            return None
        if validate_ports(raw.strip()):
            return raw.strip()
        logger.error("Porta inválida. Use: 80 ou 80,443.")


def _info(mode: str) -> str:
    if not is_info_visible():
        return ""
    return f"  {Fore.CYAN}|{Fore.BLUE} {registry.info('sniper', mode)}{Fore.RESET}"


async def sniper_menu_loop(action: str = "run") -> None:
    mode_label = "Automação" if action == "queue" else "Execução"
    m = registry.REGISTRY["sniper"]["modes"]

    while True:
        clear_terminal()
        target = global_target.value
        target_display = (
            f"{Fore.GREEN}{target}{Fore.RESET}" if target
            else f"{Fore.RED}Não definido{Fore.RESET}"
        )

        print(rf"""
        {Fore.RED}
        _____       _
        /  ___|     (_)
        \ `--. _ __  _ _ __   ___ _ __
         `--. \ '_ \| | '_ \ / _ \ '__|
        /\__/ / | | | | |_) |  __/ |    Ctrl+T → definir alvo
        \____/|_| |_|_| .__/ \___|_|    Alvo: {target_display}{Fore.RED}
                      | |               Modo: {Fore.YELLOW}{mode_label}{Fore.RED}
                      |_|
        {Fore.CYAN}[1] {Fore.RESET}{m['normal']['label']}{_info('normal')}
        {Fore.CYAN}[2] {Fore.RESET}{m['osint_recon']['label']}{_info('osint_recon')}
        {Fore.CYAN}[3] {Fore.RESET}{m['stealth']['label']}{_info('stealth')}
        {Fore.CYAN}[4] {Fore.RESET}{m['discover']['label']}{_info('discover')}
        {Fore.CYAN}[5] {Fore.RESET}{m['port']['label']}{_info('port')}
        {Fore.CYAN}[6] {Fore.RESET}{m['fullportonly']['label']}{_info('fullportonly')}
        {Fore.CYAN}[7] {Fore.RESET}{m['web']['label']}{_info('web')}
        {Fore.CYAN}[8] {Fore.RESET}{m['webporthttp']['label']}{_info('webporthttp')}
        {Fore.CYAN}[9] {Fore.RESET}{m['webporthttps']['label']}{_info('webporthttps')}
        {Fore.CYAN}[10]{Fore.RESET} {m['webscan']['label']}{_info('webscan')}
        {Fore.CYAN}[11]{Fore.RESET} {m['bruteforce']['label']}{_info('bruteforce')}
        {Fore.RED}[B] {Fore.RESET}Voltar   {Fore.YELLOW}[I]{Fore.RESET} Alternar Informações
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
            await dispatch(action, "sniper", "normal",
                           [registry.build("sniper", "normal", target)])
        elif option == "2":
            await dispatch(action, "sniper", "osint_recon",
                           [registry.build("sniper", "osint_recon", target)])
        elif option == "3":
            await dispatch(action, "sniper", "stealth",
                           [registry.build("sniper", "stealth", target)])
        elif option == "4":
            wordlist = await _get_wordlist()
            if wordlist is None:
                continue
            await dispatch(action, "sniper", "discover",
                           [registry.build("sniper", "discover", target, wordlist=wordlist)])
        elif option == "5":
            ports = await _get_ports()
            if ports is None:
                continue
            await dispatch(action, "sniper", "port",
                           [registry.build("sniper", "port", target, ports=ports)])
        elif option == "6":
            await dispatch(action, "sniper", "fullportonly",
                           [registry.build("sniper", "fullportonly", target)])
        elif option == "7":
            await dispatch(action, "sniper", "web",
                           [registry.build("sniper", "web", target)])
        elif option == "8":
            ports = await _get_ports()
            if ports is None:
                continue
            await dispatch(action, "sniper", "webporthttp",
                           [registry.build("sniper", "webporthttp", target, ports=ports)])
        elif option == "9":
            ports = await _get_ports()
            if ports is None:
                continue
            await dispatch(action, "sniper", "webporthttps",
                           [registry.build("sniper", "webporthttps", target, ports=ports)])
        elif option == "10":
            await dispatch(action, "sniper", "webscan",
                           [registry.build("sniper", "webscan", target)])
        elif option == "11":
            await dispatch(action, "sniper", "bruteforce",
                           [registry.build("sniper", "bruteforce", target)])
