from colorama import init, Fore
from functions.clear_terminal import clear_terminal
from functions.is_valid import is_valid_cidr
from functions.create_output_file import execute_command_and_log
from functions.proxy_chains import is_proxychains_enabled
from functions.set_global_target import state, set_global_target
from functions.toggle_info import toggle_info, is_info_visible
from functions.validate_ports import validate_ports
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
        'normal': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Normal Mode: Executa o scanner padrão no alvo.",
        'osint_recon': f"{Fore.CYAN}| [INFO] {Fore.BLUE}OSINT + Recon Mode: Coleta informações públicas (OSINT) e realiza reconhecimento no alvo.",
        'stealth': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Stealth Mode: Realiza uma varredura furtiva, evitando detecção, com OSINT e Recon.",
        'discover': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Discover Mode: Descobre ativos de rede e varre o CIDR fornecido, organizando em workspaces.",
        'port': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Port Scan: Varre uma porta específica do alvo.",
        'fullportonly': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Full Port Scan: Realiza uma varredura completa em todas as portas abertas do alvo.",
        'web': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Web Mode: Faz uma análise nas portas 80 (HTTP) e 443 (HTTPS) do alvo.",
        'webporthttp': f"{Fore.CYAN}| [INFO] {Fore.BLUE}HTTP Web Port Scan: Varre uma porta específica do alvo no protocolo HTTP.",
        'webporthttps': f"{Fore.CYAN}| [INFO] {Fore.BLUE}HTTPS Web Port Scan: Varre uma porta específica do alvo no protocolo HTTPS.",
        'webscan': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Web Scan Mode: Realiza uma varredura completa em busca de vulnerabilidades web no alvo.",
        'bruteforce': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Bruteforce Mode: Realiza ataques de força bruta para tentar descobrir senhas no alvo."
    }
    return explanations.get(mode, f"{Fore.RED}| [INFO] Modo não identificado.")

def sniper(target, mode, additional_param=None):
    base_command = "sudo sniper " if not is_proxychains_enabled() else "sudo proxychains sniper "
    
    commands = {
        'normal': f"{base_command}-t {target}",
        'osint_recon': f"{base_command}-t {target} -o -re",
        'stealth': f"{base_command}-t {target} -m stealth -o -re",
        'discover': f"{base_command}-t {target} -m discover -w {additional_param}",
        'port': f"{base_command}-t {target} -m port -p {additional_param}",
        'fullportonly': f"{base_command}-t {target} -fp",
        'web': f"{base_command}-t {target} -m web",
        'webporthttp': f"{base_command}-t {target} -m webporthttp -p {additional_param}",
        'webporthttps': f"{base_command}-t {target} -m webporthttps -p {additional_param}",
        'webscan': f"{base_command}-t {target} -m webscan",
        'bruteforce': f"{base_command}-t {target} -b"
    }

    command = commands.get(mode)
    if command:
        execute_command_and_log(command, "sniper")

def get_target(global_target):
    return global_target if global_target else input(f"{Fore.GREEN}Digite o alvo ou {Fore.RED}[B]{Fore.GREEN} para voltar:{Fore.RESET} ")

def get_cidr():
    while True:
        cidr = input(f"{Fore.GREEN}Digite o CIDR (EX: 192.168.0.0/24) ou {Fore.RED}[B]{Fore.GREEN} para voltar:{Fore.RESET} ").strip()
        if cidr.lower() == 'b':
            return 'b'
        if is_valid_cidr(cidr):
            return cidr
        else:
            print(f"{Fore.RED}[ERROR] CIDR inválido!{Fore.RESET}")

def get_workspace():
    return input(f"{Fore.GREEN}Digite o nome do Workspace ou {Fore.RED}[B]{Fore.GREEN} para voltar:{Fore.RESET} ")

def get_port():
    while True:
        port_string = input(f"{Fore.GREEN}Digite o número da porta ou {Fore.RED}[B]{Fore.GREEN} para voltar:{Fore.RESET} ").strip()
        if port_string.lower() == 'b':
            return 'b'
        if validate_ports(port_string):
            return int(port_string)
        else:
           print(f"{Fore.RED}[ERROR] Porta inválida (1-65536).{Fore.RESET}")

def sniper_options(option, global_target):
    target = get_target(global_target)
    if target.lower() == 'b':
        clear_terminal()
        return  
    
    if option == "1":
        sniper(target, 'normal')
    elif option == "2":
        sniper(target, 'osint_recon')
    elif option == "3":
        sniper(target, 'stealth')
    elif option == "4":
        cidr = get_cidr()
        if cidr.lower() == 'b':
            clear_terminal()
            return  
        workspace = get_workspace()
        if workspace.lower() == 'b':
            clear_terminal()
            return  
        sniper(cidr, 'discover', workspace)
    elif option == "5":
        port = get_port()
        if port == 'b':
            clear_terminal()
            return  
        sniper(target, 'port', port)
    elif option == "6":
        sniper(target, 'fullportonly')
    elif option == "7":
        sniper(target, 'web')
    elif option == "8":
        port = get_port()
        if port == 'b':
            clear_terminal()
            return  
        sniper(target, 'webporthttp', port)
    elif option == "9":
        port = get_port()
        if port == 'b':
            clear_terminal()
            return  
        sniper(target, 'webporthttps', port)
    elif option == "10":
        sniper(target, 'webscan')
    elif option == "11":
        sniper(target, 'bruteforce')
async def sniper_menu_loop(global_target):
    while True:
        clear_terminal()
        global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"

        print(rf"""
        {Fore.BLUE}
         _____       _                 
        / ____|     (_)                Pressione Ctrl+T para definir o alvo
        | (___  _ __  _ _ __   ___ _ __  {Fore.YELLOW}{global_target_display}{Fore.BLUE}
        \___ \| '_ \| | '_ \ / _ \ '__|
        ____) | | | | | |_) |  __/ |   
       |_____/|_| |_|_| .__/ \___|_|   
                      | |              
                      |_|              

        {Fore.CYAN}[1] {Fore.RESET}MODO PADRÃO {get_command_explanation('normal') if is_info_visible() else ""}
        {Fore.CYAN}[2] {Fore.RESET}MODO OSINT + RECONHECIMENTO {get_command_explanation('osint_recon') if is_info_visible() else ""}
        {Fore.CYAN}[3] {Fore.RESET}MODO FURTIVO + OSINT + RECONHECIMENTO {get_command_explanation('stealth') if is_info_visible() else ""}
        {Fore.CYAN}[4] {Fore.RESET}MODO DE DESCOBERTA {get_command_explanation('discover') if is_info_visible() else ""}
        {Fore.CYAN}[5] {Fore.RESET}ESCANEAR APENAS PORTA ESPECÍFICA {get_command_explanation('port') if is_info_visible() else ""}
        {Fore.CYAN}[6] {Fore.RESET}ESCANEAR TODAS AS PORTAS ABERTAS {get_command_explanation('fullportonly') if is_info_visible() else ""}
        {Fore.CYAN}[7] {Fore.RESET}MODO WEB {get_command_explanation('web') if is_info_visible() else ""}
        {Fore.CYAN}[8] {Fore.RESET}ESCANEAR PORTA HTTP {get_command_explanation('webporthttp') if is_info_visible() else ""}
        {Fore.CYAN}[9] {Fore.RESET}ESCANEAR PORTA HTTPS {get_command_explanation('webporthttps') if is_info_visible() else ""}
        {Fore.CYAN}[10] {Fore.RESET}ESCANEAR VULNERABILIDADES WEB {get_command_explanation('webscan') if is_info_visible() else ""}
        {Fore.CYAN}[11] {Fore.RESET}FORÇA BRUTA {get_command_explanation('bruteforce') if is_info_visible() else ""}
        {Fore.RED}[B] {Fore.RESET}Voltar
        {Fore.YELLOW}[I] {Fore.RESET}Alternar Informações
        """)

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)
        
        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option in [str(i) for i in range(1, 12)]:
            sniper_options(option, state['global_target'])
