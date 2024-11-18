from colorama import init, Fore
from functions.clear_terminal import clear_terminal
from functions.create_output_file import execute_command_and_log
from functions.proxy_chains import is_proxychains_enabled
from functions.set_global_target import state, set_global_target
from functions.toggle_info import toggle_info, is_info_visible
from functions.validate_protocol import validate_url, validate_domain_extension
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
import asyncio

init(autoreset=True)  # inicia o colorama

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
    }
    return explanations.get(mode, f"{Fore.RED}| [INFO] Modo não identificado.")


def wpscan(target, mode, api_token=None):
    base_command = "wpscan" if not is_proxychains_enabled() else "proxychains4 wpscan"
    
    commands = {
        'normal': f"{base_command} --url {target}",
        'enumerate_users': f"{base_command} --url {target} --enumerate u",
        'enumerate_plugins': f"{base_command} --url {target} --enumerate p",
        'enumerate_themes': f"{base_command} --url {target} --enumerate t",
        'scan': f"{base_command} --url {target} --api-token {api_token}"
    }

    command = commands.get(mode)
    if command:
        execute_command_and_log(command, "wpscan")

def get_api_token():
    return input(f"{Fore.GREEN}Digite seu API Token ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def wpscan_options(option, global_target):
    target = state['global_target'] if state['global_target'] else input(f"{Fore.RED}Digite o alvo ou [B] para voltar: ")
    if target.lower() == 'b':
        clear_terminal()
        return  
    
    if option == "1":
        clear_terminal()
        wpscan(target, 'normal')
    elif option == "2":
        clear_terminal()
        wpscan(target, 'enumerate_users')
    elif option == "3":
        clear_terminal()
        wpscan(target, 'enumerate_plugins')
    elif option == "4":
        clear_terminal()
        wpscan(target, 'enumerate_themes')
    elif option == "5":
        clear_terminal()
        api_token = get_api_token()  # Solicita o token aqui
        if api_token.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'scan', api_token)

async def wpscan_menu_loop(global_target):
    while True:
        clear_terminal()
        if not global_target:
            target = input(f"{Fore.RED}Digite o alvo ou [B] para voltar: ").strip()
            if target.lower() == 'b':
                break
        else:
            target = global_target

        # Adiciona http:// ou https://, se necessário
        target = validate_url(target)


        clear_terminal()

        global_target_display = f"Alvo: {target}" if target else "Alvo: Não definido"

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
        {Fore.RED}[B] {Fore.RESET}Voltar
        {Fore.YELLOW}[I] {Fore.RESET}Alternar Informações
        """)

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)
        
        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option in [str(i) for i in range(1, 6)]:
            wpscan_options(option, global_target)
