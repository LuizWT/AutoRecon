from colorama import init, Fore, Style
from functions.clear_terminal import clear_terminal
from functions.create_output_file import execute_command_and_log
from functions.proxy_chains import is_proxychains_enabled

init(autoreset=True)

def show_command_explanation(mode):
    explanations = {
        'normal': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Normal Mode: Realiza uma varredura padrão em busca de vulnerabilidades no WordPress.",
        'enumerate_users': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Enumerate Users: Tenta descobrir os usuários do WordPress.",
        'enumerate_plugins': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Enumerate Plugins: Lista os plugins instalados e suas vulnerabilidades conhecidas.",
        'enumerate_themes': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Enumerate Themes: Lista os temas instalados e suas vulnerabilidades conhecidas.",
        'scan': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Scan Mode: Realiza uma varredura completa em busca de vulnerabilidades.",
    }

    print(explanations.get(mode, f"{Fore.RED}[INFO] {Style.BRIGHT}Modo não identificado."))

def wpscan(target, mode, api_token=None):
    base_command = "wpscan" if not is_proxychains_enabled() else "proxychains4 wpscan"
    
    commands = {
        'normal': f"{base_command} --url {target}",
        'enumerate_users': f"{base_command} --url {target} --enumerate u",
        'enumerate_plugins': f"{base_command} --url {target} --enumerate p",
        'enumerate_themes': f"{base_command} --url {target} --enumerate t",
        'scan': f"{base_command} --url {target} --api-token {api_token}"  # Usa o token aqui
    }

    command = commands.get(mode)
    if command:
        print(f"{Fore.CYAN}[INFO] Executando comando: {command}")
        execute_command_and_log(command, "wpscan")

def get_target():
    return input(f"{Fore.GREEN}Digite o endereço do alvo (EX: 192.168.0.1 | site.com) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def get_api_token():
    return input(f"{Fore.GREEN}Digite seu API Token ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def wpscan_options(option):
    if option == "1":
        show_command_explanation('normal')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'normal')
    elif option == "2":
        show_command_explanation('enumerate_users')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'enumerate_users')
    elif option == "3":
        show_command_explanation('enumerate_plugins')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'enumerate_plugins')
    elif option == "4":
        show_command_explanation('enumerate_themes')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'enumerate_themes')
    elif option == "5":
        show_command_explanation('scan')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        api_token = get_api_token()  # Solicita o token aqui
        if api_token.lower() == 'b':
            clear_terminal()
            return  
        wpscan(target, 'scan', api_token)

def wpscan_menu_loop():
    while True:
        print(rf"""
        {Fore.BLUE}
        __          _______   _____  _____          _   _ 
        \ \        / /  __ \ / ____|/ ____|   /\   | \ | |
         \ \  /\  / /| |__) | (___ | |       /  \  |  \| |
          \ \/  \/ / |  ___/ \___ \| |      / /\ \ | . ` |
           \  /\  /  | |     ____) | |____ / ____ \| |\  |
            \/  \/   |_|    |_____/ \_____/_/    \_\_| \_|
        
        {Fore.CYAN}[1] {Fore.RESET}Modo Normal
        {Fore.CYAN}[2] {Fore.RESET}Enumerar Usuários
        {Fore.CYAN}[3] {Fore.RESET}Enumerar Plugins
        {Fore.CYAN}[4] {Fore.RESET}Enumerar Temas
        {Fore.CYAN}[5] {Fore.RESET}Scan Completo
        {Fore.RED}[B] {Fore.RESET}Voltar
        """)

        option = input(f"{Fore.YELLOW}Escolha uma opção: ")
        clear_terminal()
    
        if option.lower() == 'b':
            break

        if option in [str(i) for i in range(1, 6)]:
            wpscan_options(option)
        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida.")
