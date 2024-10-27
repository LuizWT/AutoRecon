from colorama import init, Fore, Style
from functions.create_output_file import execute_command_and_log
from functions.clear_terminal import clear_terminal

init(autoreset=True)

def show_command_explanation(mode):
    explanations = {
        'vuln_checks': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Verificações de Vulnerabilidades: Identifica vulnerabilidades conhecidas.",
        'server_modules': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Verificações de Módulos: Identifica módulos e scripts vulneráveis.",
        'config_files': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Teste de Arquivos de Configuração: Busca arquivos expostos.",
        'cookie_security': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Configurações de Cookies: Avalia segurança dos cookies.",
        'protocols': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Verificações de Protocolos: Identifica protocolos inseguros.",
        'dir_file_scan': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Varredura de Diretórios: Busca diretórios e arquivos acessíveis.",
        'third_party_scripts': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Verificações de Scripts: Identifica scripts de terceiros vulneráveis."
    }
    print(explanations.get(mode, f"{Fore.RED}[INFO] {Style.BRIGHT}Modo não identificado."))

def nikto(target, mode):
    base_command = f"nikto -h {target} "
    command = None

    if mode == 'vuln_checks':
        command = f"{base_command}-C all"
    elif mode == 'server_modules':
        command = f"{base_command}-M all"
    elif mode == 'config_files':
        command = f"{base_command}-e all"
    elif mode == 'cookie_security':
        command = f"{base_command}-C -p"
    elif mode == 'protocols':
        command = f"{base_command}-p"
    elif mode == 'dir_file_scan':
        command = f"{base_command}-d"
    elif mode == 'third_party_scripts':
        command = f"{base_command}-T"

    if command:
        execute_command_and_log(command, "nikto")


def execute_all_nikto_commands(target):

    commands = [
        f"-C all -h {target}",                     # Vulnerability checks
        f"-M all -h {target}",                     # Server modules checks
        f"-e all -h {target}",                     # Configuration files tests
        f"-C -p -h {target}",                      # Cookie security
        f"-p -h {target}",                         # Protocols checks
        f"-d -h {target}",                         # Directory and file scan
        f"-T -h {target}"                          # Third-party scripts checks
    ]

    for cmd in commands:
        execute_command_and_log(f"nikto {cmd}", "nikto")

def nikto_options(option):
    if option == "1":
        clear_terminal()
        show_command_explanation('vuln_checks')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'vuln_checks')
    elif option == "2":
        clear_terminal()
        show_command_explanation('server_modules')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'server_modules')
    elif option == "3":
        clear_terminal()
        show_command_explanation('config_files')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'config_files')
    elif option == "4":
        clear_terminal()
        show_command_explanation('cookie_security')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'cookie_security')
    elif option == "5":
        clear_terminal()
        show_command_explanation('protocols')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'protocols')
    elif option == "6":
        clear_terminal()
        show_command_explanation('dir_file_scan')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'dir_file_scan')
    elif option == "7":
        clear_terminal()
        show_command_explanation('third_party_scripts')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nikto(target, 'third_party_scripts')
    elif option == "8":
        clear_terminal()
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        execute_all_nikto_commands(target)

def get_target():
    return input(f"{Fore.GREEN}Digite o endereço do alvo (EX: 192.168.0.1 | site.com) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def nikto_menu_loop():
    while True:
        print(rf"""
        {Fore.BLUE}
          _   _ _ _    _        
         | \ | (_) |  | |       
         |  \| |_| | _| |_ ___  
         | . ` | | |/ / __/ _ \ 
         | |\  | |   <| || (_) |
         |_| \_|_|_|\_\\__\___/ 
                                
        {Fore.CYAN}[1] {Fore.RESET}VERIFICAÇÕES DE VULNERABILIDADES
        {Fore.CYAN}[2] {Fore.RESET}VERIFICAÇÕES DE MÓDULOS
        {Fore.CYAN}[3] {Fore.RESET}TESTE DE ARQUIVOS DE CONFIGURAÇÃO
        {Fore.CYAN}[4] {Fore.RESET}CONFIGURAÇÕES DE COOKIES
        {Fore.CYAN}[5] {Fore.RESET}VERIFICAÇÕES DE PROTOCOLOS
        {Fore.CYAN}[6] {Fore.RESET}VARREDURA DE DIRETÓRIOS
        {Fore.CYAN}[7] {Fore.RESET}VERIFICAÇÕES DE SCRIPTS DE TERCEIROS
        {Fore.CYAN}[8] {Fore.RESET}EXECUTAR TODOS OS COMANDOS
        {Fore.RED}[B] {Fore.RESET}Voltar
        """)

        option = input(f"{Fore.YELLOW}Escolha uma opção: ")

        if option.lower() == 'b':
            break

        if option in [str(i) for i in range(1, 9)]:
            nikto_options(option)
        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida.")
