from dataclasses import dataclass
from colorama import init, Fore
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
import asyncio

from functions.clear_terminal import clear_terminal
from functions.runner import run_command
from functions.logger import get_logger
from functions.proxy_chains import ProxyManager
from functions.set_global_target import global_target, set_global_target
from functions.toggle_info import toggle_info, is_info_visible

init(autoreset=True)  # inicia o colorama

logger = get_logger(__name__)
session = PromptSession()
bindings = KeyBindings()

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())

def get_command_explanation(mode):
    explanations = {
        'normal': f"{Fore.CYAN}| [INFO] {Fore.BLUE} Realiza uma varredura padrão em busca de vulnerabilidades no WordPress.",
        'enumerate_users': f"{Fore.CYAN}| [INFO] {Fore.BLUE} Tenta descobrir os usuários do WordPress.",
        'enumerate_plugins': f"{Fore.CYAN}| [INFO] {Fore.BLUE} Lista os plugins instalados e suas vulnerabilidades conhecidas.",
        'enumerate_themes': f"{Fore.CYAN}| [INFO] {Fore.BLUE} Lista os temas instalados e suas vulnerabilidades conhecidas.",
        'scan': f"{Fore.CYAN}| [INFO] {Fore.BLUE} Realiza uma varredura completa em busca de vulnerabilidades.",
        'update': f"{Fore.CYAN}| [INFO] {Fore.BLUE} Atualiza o WPSCAN.",
    }
    return explanations.get(mode, f"{Fore.RED}| [INFO] Modo não identificado.")

async def wpscan(target: str, mode: str, api_token: str = None):
    base = "sudo wpscan" if not ProxyManager.is_enabled() else "sudo proxychains wpscan"
    cmds = {
        'normal': f"{base} --url {target}",
        'enumerate_users': f"{base} --url {target} --enumerate u",
        'enumerate_plugins': f"{base} --url {target} --enumerate p",
        'enumerate_themes': f"{base} --url {target} --enumerate t",
        'scan': f"{base} --url {target} --api-token {api_token}",
        'update': f"{base} --update"
    }
    cmd = cmds.get(mode)
    if cmd:
        await run_command(cmd, "wpscan")

def get_api_token():
    return input(f"{Fore.GREEN}Digite seu API Token ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

async def wpscan_options(option: str):
    if option.lower() == 'a':
        await wpscan(target="", mode="update")
        return

    target = global_target.value or ''
    if not target:
        target = await session.prompt_async(f"{Fore.RED}Digite o alvo ou [B] para voltar: ")
        if target.lower() == 'b':
            clear_terminal()
            return

    if option == '5':
        api = await session.prompt_async(f"{Fore.GREEN}Digite seu API Token ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")
        if api.lower() == 'b':
            clear_terminal()
            return
        await wpscan(target, 'scan', api)
    else:
        modes = {'1': 'normal', '2': 'enumerate_users', '3': 'enumerate_plugins', '4': 'enumerate_themes'}
        mode = modes.get(option)
        if mode:
            await wpscan(target, mode)


async def wpscan_menu_loop(dummy_arg=None):
    while True:
        clear_terminal()

        global_target_display = (
            f"Alvo: {Fore.GREEN}{global_target.value}{Fore.RESET}"
            if global_target.value
            else f"Alvo: {Fore.RED}Não definido{Fore.RESET}"
        )

        print(rf"""
        {Fore.BLUE}
        __          _______   _____  _____          _   _ Pressione Ctrl+T para definir o alvo
        \ \        / /  __ \ / ____|/ ____|   /\   | \ | |       {Fore.YELLOW}{global_target_display}{Fore.BLUE}
         \ \  /\  / /| |__) | (___ | |       /  \  |  \| |
          \ \/  \/ / |  ___/ \___ \| |      / /\ \ | . ` |
           \  /\  /  | |     ____) | |____ / ____ \| |\  |
            \/  \/   |_|    |_____/ \_____/_/    \_\_| \_|
        
        {Fore.CYAN}[1] {Fore.RESET}Modo Normal {get_command_explanation("normal") if is_info_visible() else ""}
        {Fore.CYAN}[2] {Fore.RESET}Enumerar Usuários {get_command_explanation("enumerate_users") if is_info_visible() else ""}
        {Fore.CYAN}[3] {Fore.RESET}Enumerar Plugins {get_command_explanation("enumerate_plugins") if is_info_visible() else ""}
        {Fore.CYAN}[4] {Fore.RESET}Enumerar Temas {get_command_explanation("enumerate_themes") if is_info_visible() else ""}
        {Fore.CYAN}[5] {Fore.RESET}Scan Completo {get_command_explanation("scan") if is_info_visible() else ""}
        {Fore.CYAN}[A] {Fore.RESET}Atualizar WPSCAN {get_command_explanation("update") if is_info_visible() else ""}
        {Fore.RED}[B] {Fore.RESET}Voltar
        {Fore.YELLOW}[I] {Fore.RESET}Alternar Informações
        """)

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)
        
        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option.lower() in [str(i) for i in range(1, 6)] + ['a']:
            await wpscan_options(option)
