from colorama import init, Fore
from functions.clear_terminal import clear_terminal
from functions.create_output_file import execute_command_and_log
from functions.proxy_chains import is_proxychains_enabled
from functions.check_cidr import is_valid_cidr
from functions.set_global_target import state, set_global_target
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
        'target_spec': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varredura padrão: Varre IPs, intervalos, CIDR, arquivos, etc.",
        'scan_technique': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Técnicas de Varredura: Varredura TCP, UDP, ACK, etc.",
        'host_discovery': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Descoberta de Hosts: Descobre hosts ativos na rede.",
        'port_spec': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Especificação de Portas: Varre portas específicas ou uma faixa de portas.",
        'service_detection': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Detecção de Serviços: Detecta serviços e versões em execução.",
        'os_detection': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Detecção de SO: Tenta identificar o sistema operacional do alvo.",
        'timing': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Tempos e Desempenho: Ajusta a velocidade e desempenho da varredura.",
        'http_title': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varre as portas 80 e 443 para título HTTP.",
        'ssl_cert': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varre a porta 443 para certificado SSL.",
        'vuln': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varre as portas 80 e 443 para vulnerabilidades conhecidas.",
        'smb_os_discovery': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varre a porta 445 para descobrir o sistema operacional SMB.",
        'http_robots_txt': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varre as portas 80 e 443 para arquivo robots.txt.",
        'ssh_hostkey': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varre a porta 22 para chave do host SSH.",
        'dns_brute': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Realiza brute force em DNS.",
        'all_commands': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Executa todos os comandos de forma sequencial "
    }
    
    return explanations.get(mode, f"{Fore.RED}| [INFO] Modo não identificado.")

def nmap(target, mode, additional_param=None):
    base_command = "sudo nmap " if not is_proxychains_enabled() else "sudo proxychains nmap "
    command = None

    if mode == 'target_spec':
        command = f"{base_command}{target}"
    elif mode == 'scan_technique':
        if additional_param == 'all':
            techniques = ['-sS', '-sT', '-sU', '-sF', '-sN', '-sX']
            for technique in techniques:
                command = f"{base_command}{technique} {target}"
                execute_command_and_log(command, "nmap")
            return 
        else:
            command = f"{base_command}{additional_param} {target}"
    elif mode == 'host_discovery':
        command = f"{base_command}-sn {target}"
    elif mode == 'port_spec':
        command = f"{base_command}-p {additional_param} {target}"
    elif mode == 'service_detection':
        command = f"{base_command}-sV {target}"
    elif mode == 'os_detection':
        command = f"{base_command}-O {target}"
    elif mode == 'timing':
        command = f"{base_command}-T {additional_param} {target}"
    elif mode == 'http_title':
        command = f"{base_command}-p 80,443 --script=http-title {target}"
    elif mode == 'ssl_cert':
        command = f"{base_command}-p 443 --script=ssl-cert {target}"
    elif mode == 'vuln':
        command = f"{base_command}-p 80,443 --script=vuln {target}"
    elif mode == 'smb_os_discovery':
        command = f"{base_command}-p 445 --script=smb-os-discovery {target}"
    elif mode == 'http_robots_txt':
        command = f"{base_command}-p 80,443 --script=http-robots.txt {target}"
    elif mode == 'ssh_hostkey':
        command = f"{base_command}-p 22 --script=ssh-hostkey {target}"
    elif mode == 'dns_brute':
        command = f"{base_command}--script=dns-brute --script-args dns-brute.domain={target}"

    if command:
        execute_command_and_log(command, "nmap")

def execute_all_nmap_commands(target):
    # Os comandos DEVEM ser executados um a um para não causar conflito com a flag -p
    commands = [
        f"-sS -v {target}",                      # TCP SYN scan
        f"-sT -v {target}",                      # TCP connect scan
        f"-sU -v {target}",                      # UDP scan
        f"-sF -v {target}",                      # TCP FIN scan
        f"-sN -v {target}",                      # TCP NULL scan
        f"-sX -v {target}",                      # TCP Xmas scan
        f"-sn -v {target}",                      # Host discovery
        f"-sV -v {target}",                      # Service version detection
        f"-O -v {target}",                       # OS detection
        f"-p- -v --script=http-title {target}",  # HTTP Title em todas as portas
        f"-p 443 -v --script=ssl-cert {target}", # SSL Cert
        f"-p- -v --script=vuln {target}",        # Vulnerability scan em todas as portas
        f"-p 445 -v --script=smb-os-discovery {target}", # SMB OS discovery
        f"-p- -v --script=http-robots.txt {target}", # HTTP robots.txt em todas as portas
        f"-p 22 -v --script=ssh-hostkey {target}", # SSH Hostkey
        f"--script=dns-brute --script-args dns-brute.domain={target}" # DNS Brute Force
    ]

    for cmd in commands:
        execute_command_and_log(f"sudo nmap {cmd}", "nmap")

def nmap_options(option, global_target):
    target = state['global_target'] if state['global_target'] else input(f"{Fore.RED}Digite o alvo ou [B] para voltar: ")

    if option == "1":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return
        nmap(target, 'target_spec')
    elif option == "2":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return
        technique = get_scan_technique()
        if technique.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'scan_technique', technique)
    elif option == "4":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        ports = get_ports()
        if ports.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'port_spec', ports)
    elif option == "5":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'service_detection')  
    elif option == "6":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'os_detection')  
    elif option == "7":
        while True:
            clear_terminal()
            timing = input(f"{Fore.GREEN}Digite o nível de timing (0-5) ou {Fore.RED}[B] {Fore.GREEN}para voltar: ")
            if timing.lower() == 'b':
                clear_terminal()
                return
            if timing.isdigit() and 0 <= int(timing) <= 5:
                print(f"{Fore.GREEN}Configuração de temporização definida para {timing}.")
                nmap(target, 'timing', timing)
            else:
                print(f"{Fore.RED}Nível de timing inválido.")
    elif option == "8":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'http_title')  
    elif option == "9":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'ssl_cert')  
    elif option == "10":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'vuln')  
    elif option == "11":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'smb_os_discovery')  
    elif option == "12":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'http_robots_txt')  
    elif option == "13":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'ssh_hostkey')  
    elif option == "14":
        clear_terminal()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'dns_brute')  
    elif option == "15":
        clear_terminal()
        execute_all_nmap_commands(target)
    else:
        print(f"{Fore.RED}[INFO] {Fore.BLUE}Opção inválida!")


def get_range():
    while True:
        target = input(f"{Fore.GREEN}Digite o alvo da rede (EX: 192.168.1.0/24) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")
        if target.lower() == 'b':
            return None
        if is_valid_cidr(target):
            return target
        else:
            print(f"{Fore.RED}Formato inválido. Por favor, insira um endereço CIDR válido.")

def get_ports():
    return input(f"{Fore.GREEN}Digite as portas ou faixa de portas (EX: 21,22 ou 1-100) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def get_scan_technique():
    print(f"""
    {Fore.CYAN}[1] {Fore.RESET}-sS (TCP SYN Scan)
    {Fore.CYAN}[2] {Fore.RESET}-sT (TCP Connect Scan)
    {Fore.CYAN}[3] {Fore.RESET}-sU (UDP Scan)
    {Fore.CYAN}[4] {Fore.RESET}-sF (TCP FIN Scan)
    {Fore.CYAN}[5] {Fore.RESET}-sN (TCP NULL Scan)
    {Fore.CYAN}[6] {Fore.RESET}-sX (TCP Xmas Scan)
    {Fore.CYAN}[7] {Fore.RESET}Todas as técnicas (-sS, -sT, -sU, -sF, -sN, -sX)
    """)
    choice = input(f"{Fore.GREEN}Escolha uma técnica ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")
    
    if choice.lower() == 'b':
        return 'b'
    elif choice == '1':
        return '-sS'
    elif choice == '2':
        return '-sT'
    elif choice == '3':
        return '-sU'
    elif choice == '4':
        return '-sF'
    elif choice == '5':
        return '-sN'
    elif choice == '6':
        return '-sX'
    elif choice == '7':
        return 'all'
    else:
        print(f"{Fore.RED}[ERRO] Opção inválida. Tente novamente.")
        return get_scan_technique()

async def nmap_menu_loop(global_target):
    while True:
        clear_terminal()
        global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"  # Move this inside the loop

        print(rf"""
        {Fore.BLUE}                  
        _ __  _ __ ___   __ _ _ __   Pressione Ctrl+T para definir o alvo
        | '_ \| '_ ` _ \ / _` | '_ \       {Fore.YELLOW}{global_target_display}{Fore.BLUE}
        | | | | | | | | | (_| | |_) |
        |_| |_|_| |_| |_|\__,_| .__/ 
                              | |    
                              |_|    
                            
        {Fore.CYAN}[1] {Fore.RESET}VARREDURA PADRÃO {get_command_explanation('target_spec') if is_info_visible() else ""}
        {Fore.CYAN}[2] {Fore.RESET}TÉCNICAS DE VARREDURA {get_command_explanation('scan_technique') if is_info_visible() else ""}
        {Fore.CYAN}[3] {Fore.RESET}DESCOBRIR HOSTS {get_command_explanation('host_discovery') if is_info_visible() else ""}
        {Fore.CYAN}[4] {Fore.RESET}ESPECIFICAÇÃO DE PORTAS {get_command_explanation('port_spec') if is_info_visible() else ""}
        {Fore.CYAN}[5] {Fore.RESET}DETEÇÃO DE SERVIÇOS {get_command_explanation('service_detection') if is_info_visible() else ""}
        {Fore.CYAN}[6] {Fore.RESET}DETEÇÃO DE SISTEMA OPERACIONAL {get_command_explanation('os_detection') if is_info_visible() else ""}
        {Fore.CYAN}[7] {Fore.RESET}TEMPORIZAÇÃO E DESEMPENHO {get_command_explanation('timing') if is_info_visible() else ""}
        {Fore.CYAN}[8] {Fore.RESET}HTTP TITLE {get_command_explanation('http_title') if is_info_visible() else ""}
        {Fore.CYAN}[9] {Fore.RESET}SSL CERT {get_command_explanation('ssl_cert') if is_info_visible() else ""}
        {Fore.CYAN}[10] {Fore.RESET}VULN {get_command_explanation('vuln') if is_info_visible() else ""}
        {Fore.CYAN}[11] {Fore.RESET}SMB OS DISCOVERY {get_command_explanation('smb_os_discovery') if is_info_visible() else ""}
        {Fore.CYAN}[12] {Fore.RESET}HTTP ROBOTS.TXT {get_command_explanation('http_robots_txt') if is_info_visible() else ""}
        {Fore.CYAN}[13] {Fore.RESET}SSH HOSTKEY {get_command_explanation('ssh_hostkey') if is_info_visible() else ""}
        {Fore.CYAN}[14] {Fore.RESET}DNS BRUTE FORCE {get_command_explanation('dns_brute') if is_info_visible() else ""}
        {Fore.CYAN}[15] {Fore.RESET}EXECUTAR TODOS OS COMANDOS {get_command_explanation('all_commands') if is_info_visible() else ""}
        {Fore.RED}[B] {Fore.RESET}Voltar
        {Fore.YELLOW}[I] {Fore.RESET}Alternar Informações
        """)

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)

        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue

        if option in [str(i) for i in range(1, 16)]:
            nmap_options(option, global_target)
