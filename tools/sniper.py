from colorama import init, Fore, Style
import os
import platform

init(autoreset=True)

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

output_dir = "output"
output_file = os.path.join(output_dir, "sn1per_output.txt")
os.makedirs(output_dir, exist_ok=True)

def execute_command_and_log(command):
    """Executa um comando e registra a saída no arquivo de log."""
    full_command = f"{command} >> {output_file} 2>&1"
    print(f"{Fore.YELLOW}Executando comando: {full_command}")
    os.system(full_command)

def show_command_explanation(mode):
    explanations = {
        'normal': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Normal Mode: Executa o scanner padrão no alvo.",
        'osint_recon': f"{Fore.CYAN}[INFO] {Style.BRIGHT}OSINT + Recon Mode: Coleta informações públicas (OSINT) e realiza reconhecimento no alvo.",
        'stealth': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Stealth Mode: Realiza uma varredura furtiva, evitando detecção, com OSINT e Recon.",
        'discover': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Discover Mode: Descobre ativos de rede e varre o CIDR fornecido, organizando em workspaces.",
        'port': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Port Scan: Varre uma porta específica do alvo.",
        'fullportonly': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Full Port Scan: Realiza uma varredura completa em todas as portas abertas do alvo.",
        'web': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Web Mode: Faz uma análise nas portas 80 (HTTP) e 443 (HTTPS) do alvo.",
        'webporthttp': f"{Fore.CYAN}[INFO] {Style.BRIGHT}HTTP Web Port Scan: Varre uma porta específica do alvo no protocolo HTTP.",
        'webporthttps': f"{Fore.CYAN}[INFO] {Style.BRIGHT}HTTPS Web Port Scan: Varre uma porta específica do alvo no protocolo HTTPS.",
        'webscan': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Web Scan Mode: Realiza uma varredura completa em busca de vulnerabilidades web no alvo.",
        'bruteforce': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Bruteforce Mode: Realiza ataques de força bruta para tentar descobrir senhas no alvo."
    }

    print(explanations.get(mode, f"{Fore.RED}[INFO] {Style.BRIGHT}Modo não identificado."))

def sniper(target, mode, additional_param=None):
    base_command = "sudo sniper "
    if mode == 'normal':
        command = f"{base_command}-t {target}"
    elif mode == 'osint_recon':
        command = f"{base_command}-t {target} -o -re"
    elif mode == 'stealth':
        command = f"{base_command}-t {target} -m stealth -o -re"
    elif mode == 'discover':
        command = f"{base_command}-t {target} -m discover -w {additional_param}"
    elif mode == 'port':
        command = f"{base_command}-t {target} -m port -p {additional_param}"
    elif mode == 'fullportonly':
        command = f"{base_command}-t {target} -fp"
    elif mode == 'web':
        command = f"{base_command}-t {target} -m web"
    elif mode == 'webporthttp':
        command = f"{base_command}-t {target} -m webporthttp -p {additional_param}"
    elif mode == 'webporthttps':
        command = f"{base_command}-t {target} -m webporthttps -p {additional_param}"
    elif mode == 'webscan':
        command = f"{base_command}-t {target} -m webscan"
    elif mode == 'bruteforce':
        command = f"{base_command}-t {target} -b"
    else:
        command = None

    if command:
        execute_command_and_log(command)

def get_target():
    return input(f"{Fore.GREEN}Digite o endereço do alvo (EX: 192.168.0.1 | site.com) ou [B] para voltar: ")

def get_cidr():
    return input(f"{Fore.GREEN}Digite o CIDR (EX: 192.168.0.0/24) ou [B] para voltar: ")

def get_workspace():
    return input(f"{Fore.GREEN}Digite o nome do Workspace ou [B] para voltar: ")

def get_port():
    return input(f"{Fore.GREEN}Digite o número da porta ou [B] para voltar: ")

def sniper_options(option):
    if option == "1":
        show_command_explanation('normal')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'normal')
    elif option == "2":
        show_command_explanation('osint_recon')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'osint_recon')
    elif option == "3":
        show_command_explanation('stealth')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'stealth')
    elif option == "4":
        show_command_explanation('discover')
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
        show_command_explanation('port')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        port = get_port()
        if port.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'port', port)
    elif option == "6":
        show_command_explanation('fullportonly')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'fullportonly')
    elif option == "7":
        show_command_explanation('web')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'web')
    elif option == "8":
        show_command_explanation('webporthttp')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        port = get_port()
        if port.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'webporthttp', port)
    elif option == "9":
        show_command_explanation('webporthttps')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        port = get_port()
        if port.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'webporthttps', port)
    elif option == "10":
        show_command_explanation('webscan')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return  
        sniper(target, 'webscan')
    elif option == "11":
        show_command_explanation('bruteforce')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal() 
            return 
        sniper(target, 'bruteforce')

def sniper_menu_loop():
    while True:
        print(f"""
        {Fore.BLUE}︻デ═一
        {Fore.CYAN}[1] {Fore.RESET}MODO NORMAL
        {Fore.CYAN}[2] {Fore.RESET}MODO OSINT + RECONHECIMENTO
        {Fore.CYAN}[3] {Fore.RESET}MODO FURTIVO + OSINT + RECONHECIMENTO
        {Fore.CYAN}[4] {Fore.RESET}MODO DE DESCOBERTA
        {Fore.CYAN}[5] {Fore.RESET}ESCANEAR APENAS PORTA ESPECÍFICA
        {Fore.CYAN}[6] {Fore.RESET}MODO DE ESCANEAMENTO COMPLETO
        {Fore.CYAN}[7] {Fore.RESET}MODO WEB (Porta 80 + 443)
        {Fore.CYAN}[8] {Fore.RESET}ESCANEAR PORTA WEB ESPECÍFICA (HTTP)
        {Fore.CYAN}[9] {Fore.RESET}ESCANEAR PORTA WEB ESPECÍFICA (HTTPS)
        {Fore.CYAN}[10] {Fore.RESET}ESCANEAR VULNERABILIDADES WEB
        {Fore.CYAN}[11] {Fore.RESET}MODO DE FORÇA BRUTA
        {Fore.RED}[B] {Fore.RESET}Voltar
        """)

        option = input(f"{Fore.YELLOW}Escolha uma opção: ")
        clear_terminal()
    
        if option.lower() == 'b':
            break

        if option in [str(i) for i in range(1, 12)]:
            sniper_options(option)
        else:
            continue