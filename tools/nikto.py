from colorama import init, Fore, Style
from functions.create_output_file import execute_command_and_log
from functions.clear_terminal import clear_terminal
from functions.set_global_target import state
from functions.toggle_info import toggle_info, is_info_visible

init(autoreset=True)  # inicia o colorama

def get_command_explanation(mode):
    explanations = {
        'vuln_checks': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Verificações de Vulnerabilidades: Identifica vulnerabilidades conhecidas.",
        'server_modules': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Verificações de Módulos: Identifica módulos e scripts vulneráveis.",
        'config_files': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Teste de Arquivos de Configuração: Busca arquivos expostos.",
        'cookie_security': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Configurações de Cookies: Avalia segurança dos cookies.",
        'protocols': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Verificações de Protocolos: Identifica protocolos inseguros.",
        'dir_file_scan': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varredura de Diretórios: Busca diretórios e arquivos acessíveis.",
        'third_party_scripts': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Verificações de Scripts: Identifica scripts de terceiros vulneráveis.",
        'all_commands': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Executa todos os comandos de forma sequencial "
    }
    return explanations.get(mode, f"{Fore.RED}| [INFO] Modo não identificado.")

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
    target = state['global_target'] if state['global_target'] else input(f"{Fore.RED}Digite o alvo: ")
    clear_terminal()
    if option == "1":
        nikto(target, 'vuln_checks')
    elif option == "2":
        nikto(target, 'server_modules')
    elif option == "3":
        nikto(target, 'config_files')
    elif option == "4":
        nikto(target, 'cookie_security')
    elif option == "5":
        nikto(target, 'protocols')
    elif option == "6":
        nikto(target, 'dir_file_scan')
    elif option == "7":
        nikto(target, 'third_party_scripts')
    elif option == "8":
        execute_all_nikto_commands(target)

def nikto_menu_loop(global_target):
    global_target_display = f"Alvo: {global_target}" if global_target else "Alvo: Não definido"
    while True:
        clear_terminal()
        print(rf"""
        {Fore.BLUE}
          _   _ _ _    _        
         | \ | (_) |  | |       {Fore.YELLOW}{global_target_display}{Fore.BLUE}
         |  \| |_| | _| |_ ___  
         | . ` | | |/ / __/ _ \ 
         | |\  | |   <| || (_) |
         |_| \_|_|_|\_\\__\___/ 
                                
        {Fore.CYAN}[1] {Fore.RESET}VERIFICAÇÕES DE VULNERABILIDADES {get_command_explanation('vuln_checks') if is_info_visible() else ""}
        {Fore.CYAN}[2] {Fore.RESET}VERIFICAÇÕES DE MÓDULOS {get_command_explanation('server_modules') if is_info_visible() else ""}
        {Fore.CYAN}[3] {Fore.RESET}TESTE DE ARQUIVOS DE CONFIGURAÇÃO {get_command_explanation('config_files') if is_info_visible() else ""}
        {Fore.CYAN}[4] {Fore.RESET}CONFIGURAÇÕES DE COOKIES {get_command_explanation('cookie_security') if is_info_visible() else ""}
        {Fore.CYAN}[5] {Fore.RESET}VERIFICAÇÕES DE PROTOCOLOS {get_command_explanation('protocols') if is_info_visible() else ""}
        {Fore.CYAN}[6] {Fore.RESET}VARREDURA DE DIRETÓRIOS {get_command_explanation('dir_file_scan') if is_info_visible() else ""}
        {Fore.CYAN}[7] {Fore.RESET}VERIFICAÇÕES DE SCRIPTS DE TERCEIROS {get_command_explanation('third_party_scripts') if is_info_visible() else ""}
        {Fore.CYAN}[8] {Fore.RESET}EXECUTAR TODOS OS COMANDOS {get_command_explanation('all_commands') if is_info_visible() else ""}
        {Fore.RED}[B] {Fore.RESET}Voltar
        {Fore.YELLOW}[I] {Fore.RESET}Alternar Informações
        """)

        option = input(f"{Fore.YELLOW}Escolha uma opção: ")

        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option in [str(i) for i in range(1, 9)]:
            nikto_options(option)
        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida.")
