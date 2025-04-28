from colorama import init, Fore
from functions.create_output_file import execute_command_and_log
from functions.clear_terminal import clear_terminal
from functions.set_global_target import set_global_target, global_target
from functions.toggle_info import toggle_info, is_info_visible
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
    target = global_target.value or input(f"{Fore.RED}Digite o alvo: ")
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

async def nikto_menu_loop():
    while True:
        clear_terminal()
        global_target_display = (
            f"Alvo: {Fore.GREEN}{global_target.value}{Fore.RESET}"
            if global_target.value
            else f"Alvo: {Fore.RED}Não definido{Fore.RESET}"
        )
        print(rf"""
        {Fore.BLUE}
          _   _ _ _    _        
         | \ | (_) |  | |   Pressione Ctrl+T para definir o alvo
         |  \| |_| | _| |_ ___  {Fore.YELLOW}{global_target_display}{Fore.BLUE}
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

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)

        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option in [str(i) for i in range(1, 9)]:
            nikto_options(option)
        else:
            print(f"{Fore.RED}Opção inválida.")
