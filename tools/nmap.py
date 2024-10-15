from colorama import init, Fore, Style
from functions.clear_terminal import clear_terminal
from functions.create_output_file import execute_command_and_log

init(autoreset=True)

def show_command_explanation(mode):
    explanations = {
        'target_spec': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Varredura padrão: Varre IPs, intervalos, CIDR, arquivos, etc.",
        'scan_technique': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Técnicas de Varredura: Varredura TCP, UDP, ACK, etc.",
        'host_discovery': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Descoberta de Hosts: Descobre hosts ativos na rede.",
        'port_spec': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Especificação de Portas: Varre portas específicas ou uma faixa de portas.",
        'service_detection': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Detecção de Serviços: Detecta serviços e versões em execução.",
        'os_detection': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Detecção de SO: Tenta identificar o sistema operacional do alvo.",
        'timing': f"{Fore.CYAN}[INFO] {Style.BRIGHT}Tempos e Desempenho: Ajusta a velocidade e desempenho da varredura.",
        'http_title': f"{Fore.CYAN}[INFO] {Style.BRIGHT}http-title: Varre as portas 80 e 443 para título HTTP.",
        'ssl_cert': f"{Fore.CYAN}[INFO] {Style.BRIGHT}ssl-cert: Varre a porta 443 para certificado SSL.",
        'vuln': f"{Fore.CYAN}[INFO] {Style.BRIGHT}vuln: Varre as portas 80 e 443 para vulnerabilidades conhecidas.",
        'smb_os_discovery': f"{Fore.CYAN}[INFO] {Style.BRIGHT}smb-os-discovery: Varre a porta 445 para descobrir o sistema operacional SMB.",
        'http_robots_txt': f"{Fore.CYAN}[INFO] {Style.BRIGHT}http-robots.txt: Varre as portas 80 e 443 para arquivo robots.txt.",
        'ssh_hostkey': f"{Fore.CYAN}[INFO] {Style.BRIGHT}ssh-hostkey: Varre a porta 22 para chave do host SSH.",
        'dns_brute': f"{Fore.CYAN}[INFO] {Style.BRIGHT}dns-brute: Realiza brute force em DNS."
    }
    
    print(explanations.get(mode, f"{Fore.RED}[INFO] {Style.BRIGHT}Modo não identificado."))

def nmap(target, mode, additional_param=None):
    base_command = "sudo nmap "
    command = None  # Inicializa command como None

    if mode == 'target_spec':
        command = f"{base_command}{target}"
    elif mode == 'scan_technique':
        if additional_param == 'all':
            techniques = ['-sS', '-sT', '-sU', '-sF', '-sN', '-sX']
            for technique in techniques:
                command = f"{base_command}{technique} {target}"
                execute_command_and_log(command)
            return  # Retorna para evitar executar `execute_command_and_log` novamente
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
        execute_command_and_log(command)

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
        execute_command_and_log(f"sudo nmap {cmd}")


def nmap_options(option):
    if option == "1":
        show_command_explanation('target_spec')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        nmap(target, 'target_spec')
    elif option == "2":
        show_command_explanation('scan_technique')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return
        technique = get_scan_technique()
        if technique.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'scan_technique', technique)
    elif option == "3":
        show_command_explanation('host_discovery')
        target = get_range()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'host_discovery')  
    elif option == "4":
        show_command_explanation('port_spec')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        ports = get_ports()
        if ports.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'port_spec', ports)
    elif option == "5":
        show_command_explanation('service_detection')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'service_detection')  
    elif option == "6":
        show_command_explanation('os_detection')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'os_detection')  
    elif option == "7":
        show_command_explanation('timing')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        timing = input(f"{Fore.GREEN}Digite o nível de timing (0-5) ou {Fore.RED}[B] {Fore.GREEN}para voltar: ")
        if timing.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'timing', timing)
    elif option == "8":
        execute_all_nmap_commands(get_target())
    elif option == "9":
        show_command_explanation('http_title')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'http_title')  
    elif option == "10":
        show_command_explanation('ssl_cert')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'ssl_cert')  
    elif option == "11":
        show_command_explanation('vuln')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'vuln')  
    elif option == "12":
        show_command_explanation('smb_os_discovery')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'smb_os_discovery')  
    elif option == "13":
        show_command_explanation('http_robots_txt')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'http_robots_txt')  
    elif option == "14":
        show_command_explanation('ssh_hostkey')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'ssh_hostkey')  
    elif option == "15":
        show_command_explanation('dns_brute')
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        nmap(target, 'dns_brute')  

    elif option == "15":
        target = get_target()
        if target.lower() == 'b':
            clear_terminal()
            return  
        execute_all_nmap_commands(target)

def get_target():
    return input(f"{Fore.GREEN}Digite o endereço do alvo (EX: 192.168.0.1 | site.com) ou [B] para voltar: ")

def get_range():
    return input(f"{Fore.GREEN}Digite o intervalo ou CIDR (EX: 192.168.1.0/24) ou [B] para voltar: ")

def get_ports():
    return input(f"{Fore.GREEN}Digite as portas ou faixa de portas (EX: 21,22 ou 1-100) ou [B] para voltar: ")

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
    choice = input(f"{Fore.GREEN}Escolha uma técnica ou [B] para voltar: ")
    
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


def nmap_menu_loop():
    while True:
        print(rf"""
        {Fore.BLUE}                  
        _ __  _ __ ___   __ _ _ __  
        | '_ \| '_ ` _ \ / _` | '_ \ 
        | | | | | | | | | (_| | |_) |
        |_| |_|_| |_| |_|\__,_| .__/ 
                            | |    
                            |_|    
                            
        {Fore.CYAN}[1] {Fore.RESET}VARREDURA PADRÃO
        {Fore.CYAN}[2] {Fore.RESET}TÉCNICAS DE VARREDURA
        {Fore.CYAN}[3] {Fore.RESET}DESCUBRIR HOSTS
        {Fore.CYAN}[4] {Fore.RESET}ESPECIFICAÇÃO DE PORTAS
        {Fore.CYAN}[5] {Fore.RESET}DETEÇÃO DE SERVIÇOS
        {Fore.CYAN}[6] {Fore.RESET}DETEÇÃO DE SISTEMA OPERACIONAL
        {Fore.CYAN}[7] {Fore.RESET}TEMPORIZAÇÃO E DESEMPENHO
        {Fore.CYAN}[8] {Fore.RESET}HTTP TITLE
        {Fore.CYAN}[9] {Fore.RESET}SSL CERT
        {Fore.CYAN}[10] {Fore.RESET}VULN
        {Fore.CYAN}[11] {Fore.RESET}SMB OS DISCOVERY
        {Fore.CYAN}[12] {Fore.RESET}HTTP ROBOTS.TXT
        {Fore.CYAN}[13] {Fore.RESET}SSH HOSTKEY
        {Fore.CYAN}[14] {Fore.RESET}DNS BRUTE FORCE
        {Fore.CYAN}[15] {Fore.RESET}EXECUTAR TODOS OS COMANDOS
        {Fore.RED}[B] {Fore.RESET}Voltar
        """)

        option = input(f"{Fore.GREEN}Escolha uma opção: ")


        if option.lower() == 'b':
            break

        if option in [str(i) for i in range(1, 16)]:
            nmap_options(option)
        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida.")
