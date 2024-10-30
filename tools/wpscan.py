from colorama import init, Fore, Style
from functions.clear_terminal import clear_terminal
from functions.create_output_file import execute_command_and_log
from functions.proxy_chains import is_proxychains_enabled
from functions.set_global_target import state
from functions.toggle_info import toggle_info, is_info_visible

init(autoreset=True)  # inicia o colorama

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

def get_target(global_target):
    return global_target if global_target else input(f"{Fore.RED}Digite o alvo ou [B] para voltar: ")

def get_api_token():
    return input(f"{Fore.GREEN}Digite seu API Token ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def wpscan_options(option, global_target):
    target = get_target(global_target)
    if target.lower() == 'b':
        clear_terminal()
        return  
    
    if option == "1":
        wpscan(target, 'normal')
    elif option == "2":
        wpscan(target, 'enumerate_users')
    elif option == "3":
        wpscan(target, 'enumerate_plugins')
    elif option == "4":
        wpscan(target, 'enumerate_themes')
    elif option == "5":
        api_token = get_api_token()  # Solicita o token aqui
        if api_token.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'scan', api_token)

def wpscan_menu_loop(global_target):
    while True:
        clear_terminal()
        global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"

        print(rf"""
        {Fore.BLUE}
        __          _______   _____  _____          _   _ {Fore.YELLOW}{global_target_display}{Fore.BLUE}
        \ \        / /  __ \ / ____|/ ____|   /\   | \ | |
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

        option = input(f"{Fore.YELLOW}Escolha uma opção: ")
        
        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option in [str(i) for i in range(1, 6)]:
            wpscan_options(option, global_target)
        else:
            print(f"{Fore.RED}Opção inválida.")
