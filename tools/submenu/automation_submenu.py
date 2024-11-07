import asyncio
from prompt_toolkit import PromptSession
from colorama import Fore, Style, init
from functions.clear_terminal import clear_terminal
from functions.set_global_target import state
from functions.create_output_file import execute_command_and_log_submenu
from prompt_toolkit.formatted_text import HTML

init(autoreset=True)

session = PromptSession()
is_running = False
automation_lock = asyncio.Lock()

#TODO Adicionar na biblioteca a lista de comandos para cada ferramenta

tools_commands = {
    "nmap": {
        "target_spec": {
            "command": "nmap",
            "params": lambda target: f"{target}"
        },
        "scan_technique": {
            "command": "nmap",
            "params": lambda technique, target: f"{technique} {target}",
            "all": ['-sS', '-sT', '-sU', '-sF', '-sN', '-sX'],
        },
        "host_discovery": {
            "command": "nmap",
            "params": lambda target: f"-sn {target}"
        },
        "port_spec": {
            "command": "nmap",
            "params": lambda target, port: f"-p {port} {target}"
        },
        "service_detection": {
            "command": "nmap",
            "params": lambda target: f"-sV {target}"
        },
        "os_detection": {
            "command": "nmap",
            "params": lambda target: f"-O {target}"
        },
        "timing": {
            "command": "nmap",
            "params": lambda target, level: f"-T {level} {target}"
        },
        "http_title": {
            "command": "nmap",
            "params": lambda target: f"-p 80,443 --script=http-title {target}"
        },
        "ssl_cert": {
            "command": "nmap",
            "params": lambda target: f"-p 443 --script=ssl-cert {target}"
        },
        "vuln": {
            "command": "nmap",
            "params": lambda target: f"-p 80,443 --script=vuln {target}"
        },
        "smb_os_discovery": {
            "command": "nmap",
            "params": lambda target: f"-p 445 --script=smb-os-discovery {target}"
        },
        "http_robots_txt": {
            "command": "nmap",
            "params": lambda target: f"-p 80,443 --script=http-robots.txt {target}"
        },
        "ssh_hostkey": {
            "command": "nmap",
            "params": lambda target: f"-p 22 --script=ssh-hostkey {target}"
        },
        "dns_brute": {
            "command": "nmap",
            "params": lambda target: f"--script=dns-brute --script-args dns-brute.domain={target}"
        },
        "all_commands": {
            "command": "nmap",
            "params": lambda target: [
                f"-sS -v {target}",                      # TCP SYN scan
                f"-sT -v {target}",                      # TCP connect scan
                f"-sU -v {target}",                      # UDP scan
                f"-sF -v {target}",                      # TCP FIN scan
                f"-sN -v {target}",                      # TCP NULL scan
                f"-sX -v {target}",                      # TCP Xmas scan
                f"-sn -v {target}",                      # Host discovery
                f"-sV -v {target}",                      # Service version detection
                f"-O -v {target}",                       # OS detection
                f"-p- -v --script=http-title {target}", # HTTP Title on all ports
                f"-p 443 -v --script=ssl-cert {target}", # SSL Cert
                f"-p- -v --script=vuln {target}",        # Vulnerability scan on all ports
                f"-p 445 -v --script=smb-os-discovery {target}", # SMB OS discovery
                f"-p- -v --script=http-robots.txt {target}", # HTTP robots.txt on all ports
                f"-p 22 -v --script=ssh-hostkey {target}", # SSH Hostkey
                f"--script=dns-brute --script-args dns-brute.domain={target}" # DNS Brute Force
            ]
        }
    }
}



command_queue = []

def format_command(tool, mode, target, additional_param=None):
    if mode in tools_commands[tool]:
        if mode == "scan_technique":
            return f"{tools_commands[tool][mode]['command']} {tools_commands[tool][mode]['params'](additional_param, target)}"
        elif mode == "port_spec":
            return f"{tools_commands[tool][mode]['command']} {tools_commands[tool][mode]['params'](target, additional_param)}"
        elif mode == "host_discovery":
            return f"{tools_commands[tool][mode]['command']} {tools_commands[tool][mode]['params'](target)}"
        elif mode == "timing":
            return f"{tools_commands[tool][mode]['command']} {tools_commands[tool][mode]['params'](target, additional_param)}"
        elif mode == "all_commands":
            commands = tools_commands[tool][mode]["params"](target)
            return "\n".join([f"{tools_commands[tool][mode]['command']} {cmd}" for cmd in commands])
        else:
            return f"{tools_commands[tool][mode]['command']} {tools_commands[tool][mode]['params'](target)}"
    return f"{tool} {target}" 

def add_command_to_queue(tool_name, mode, target, additional_param=None):
    formatted_command = format_command(tool_name, mode, target, additional_param)
    command_data = {
        "tool": tool_name,
        "mode": mode,
        "command": formatted_command
    }
    command_queue.append(command_data)
    clear_terminal()
    print(f"{Fore.GREEN}Comando adicionado: {formatted_command}")


async def execute_commands_in_intervals(interval_minutes):
    global is_running
    is_running = True
    print(rf"{Fore.CYAN}Iniciando automação com intervalos de {interval_minutes} minutos{'\n'}Pressione {Fore.RED}Enter{Fore.CYAN} para interromper a execução.")

    try:
        while is_running:
            for command_data in command_queue:
                if not is_running:
                    break
                await process_command(command_data)
            print(rf"{Fore.CYAN}Iniciando automação com intervalos de {interval_minutes} minutos{'\n'}Pressione {Fore.RED}Enter{Fore.CYAN} para interromper a execução.{'\n'}{Fore.YELLOW}Aguardando {interval_minutes} minutos para a próxima execução...{Fore.RESET}{'\n'}")
            await asyncio.sleep(interval_minutes * 60)
    except asyncio.CancelledError:
        clear_terminal()
        print("\nAutomação interrompida pelo usuário.\nVoltando para o Submenu...")
    except KeyboardInterrupt:
        clear_terminal()
        print("\nAutomação interrompida pelo usuário.\nVoltando para o Submenu...")
    finally:
        is_running = False


async def process_command(command_data):
    tool = command_data.get("tool")
    command = command_data.get("command")

    try:
        if tool == "custom":
            await execute_command_and_log_submenu(command, tool)
        elif tool in tools_commands:
            mode = command_data.get("mode")
            target = command_data.get("target", state.get('global_target'))
            param = command_data.get("param")

            if mode == "all_commands":
                commands = tools_commands[tool][mode]["params"](target)
                for cmd in commands:
                    await execute_command_and_log_submenu(f"{tools_commands[tool][mode]['command']} {cmd}", tool)
            elif mode == "scan_technique":
                command_func = tools_commands[tool][mode]["params"]
                command = command_func(param, target)
                await execute_command_and_log_submenu(f"{tools_commands[tool][mode]['command']} {command}", tool)
            else:
                command_func = tools_commands[tool][mode]["params"]
                command = command_func(target, param) if param else command_func(target)
                await execute_command_and_log_submenu(f"{tools_commands[tool][mode]['command']} {command}", tool)
        else:
            print(f"Modo '{mode}' não encontrado na biblioteca de comandos para '{tool}'.")
    except Exception as e:
        print(f"Erro ao executar o comando: {e}")





async def nmap_menu():
    target = state['global_target']
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
        {Fore.CYAN}[3] {Fore.RESET}DESCOBRIR HOSTS
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
        {Fore.RED}[B] {Fore.RESET}Voltar""")
        
        mode_choice = await session.prompt_async(HTML(f"<ansiyellow>\nEscolha um modo para NMAP:</ansiyellow> "))

        if mode_choice == '1':
            add_command_to_queue("nmap", "target_spec", target)
        elif mode_choice == '2':
            technique = await get_scan_technique()
            if technique.lower() == 'b':
                clear_terminal()
                continue
            add_command_to_queue("nmap", "scan_technique", target, technique)
        elif mode_choice == '3':
            add_command_to_queue("nmap", "host_discovery", target)
        elif mode_choice == '4':
            while True:
                port_input = await session.prompt_async(HTML("<ansiyellow>Digite o número da porta ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                
                if port_input.lower() == 'b':
                    clear_terminal()
                    break
                try:
                    port = int(port_input)
                    if port in range(1, 65536):
                        add_command_to_queue("nmap", "port_spec", target, port)
                        break
                    else:
                        print("Porta inválida (1-65536).")
                except ValueError:
                    print("Valor inválido, tente novamente.")
        elif mode_choice == '5':
            add_command_to_queue("nmap", "service_detection", target)
        elif mode_choice == '6':
            add_command_to_queue("nmap", "os_detection", target)
        elif mode_choice == '7':
            while True:
                level_input = await session.prompt_async(HTML("<ansiyellow>Digite o nível de velocidade (1-5) ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                
                if level_input.lower() == 'b':
                    clear_terminal()
                    break
                try:
                    level = int(level_input)
                    if level in range(1, 6):
                        add_command_to_queue("nmap", "timing", target, level)
                        break
                    else:
                        print("Nível de velocidade inválido (1-5).")
                except ValueError:
                    print("Valor inválido, tente novamente.")
        elif mode_choice == '8':
            add_command_to_queue("nmap", "http_title", target)
        elif mode_choice == '9':
            add_command_to_queue("nmap", "ssl_cert", target)
        elif mode_choice == '10':
            add_command_to_queue("nmap", "vuln", target)
        elif mode_choice == '11':
            add_command_to_queue("nmap", "smb_os_discovery", target)
        elif mode_choice == '12':
            add_command_to_queue("nmap", "http_robots_txt", target)
        elif mode_choice == '13':
            add_command_to_queue("nmap", "ssh_hostkey", target)
        elif mode_choice == '14':
            add_command_to_queue("nmap", "dns_brute", target)
        elif mode_choice == '15':
            add_command_to_queue("nmap", "all_commands", target)
        elif mode_choice.lower() == 'b':
            clear_terminal()
            return
        else:
            clear_terminal()
            print(f"{Fore.RED}[INFO] Opção inválida, tente novamente.")

async def automation_setup_menu():
    global is_running

    while True:
        print(rf"""
            {Fore.BLUE}{Style.BRIGHT}
                _        _____                      
     /\        | |      |  __ \      {Fore.GREEN}Configuração de Automação{Fore.BLUE}{Style.BRIGHT}
    /  \  _   _| |_ ___ | |__) |___  ___ ___  _ __ 
   / /\ \| | | | __/ _ \|  _  // _ \/ __/ _ \| '_ \ 
  / ____ \ |_| | || (_) | | \ \  __/ (_| (_) | | | |
 /_/    \_\__,_|\__\___/|_|  \_\___|\___\___/|_| |_|
                                            LuizWt{Style.RESET_ALL}
        
    {Fore.YELLOW}Escolha uma ferramenta para adicionar comandos à fila de automação:
    {Fore.CYAN}[1]{Fore.RESET} NMAP
    {Fore.CYAN}[A]{Fore.RESET} Iniciar Automação
    {Fore.CYAN}[Q]{Fore.RESET} Editar Queue
    {Fore.RED}[B]{Fore.RESET} Sair""")

        choice = await session.prompt_async(HTML("<ansiyellow>Escolha uma opção:</ansiyellow> "))

        if choice == '1':
            clear_terminal()
            await nmap_menu()
        elif choice.lower() == 'a':
            while True:
                interval_input = await session.prompt_async(HTML("<ansiyellow>Digite o intervalo (em minutos) ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if interval_input.lower() == 'b':
                    clear_terminal()
                    break
                try:
                    interval = int(interval_input)
                    if interval > 0:
                        await execute_commands_in_intervals(interval)
                        break
                    else:
                        print("Por favor, insira um número inteiro positivo.")
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número inteiro.")
        elif choice.lower() == 'q':
            await edit_queue_menu()
        elif choice.lower() == 'b':
            if is_running:
                print("Automação em andamento. Conclua ou interrompa a execução antes de sair.")
            else:
                clear_terminal()
                print(f"{Fore.GREEN}Saindo da configuração de automação...\nPressione {Fore.RED}Enter{Fore.GREEN} para continuar.")
                return
                
        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida, tente novamente.")



async def edit_queue_menu():
    while True:
        clear_terminal()
        if command_queue:
            print(f"{Fore.CYAN}Comandos na Fila de Automação:{Style.RESET_ALL}")
            for idx, cmd in enumerate(command_queue, start=1):
                print(f"{Fore.CYAN}[{idx}]{Fore.RESET} {cmd['command']}")
            print(f"\n{'='*50}\n{Fore.CYAN}[A]{Fore.RESET} Adicionar comando customizado\n{Fore.RED}[R]{Fore.RESET} Remover um comando\n{Fore.RED}[B]{Fore.RESET} Voltar")

            choice = await session.prompt_async(HTML("<ansiyellow>Escolha uma opção:</ansiyellow> "))

            if choice.lower() == 'r':
                await remove_command_from_queue()
            elif choice.lower() == 'a':
                await add_custom_command_to_queue()
            elif choice.lower() == 'b':
                clear_terminal()
                return
            else:
                ""
                
        else:
            print(f"{Fore.YELLOW}A fila de comandos está vazia.{Style.RESET_ALL}")
            choice = await session.prompt_async(HTML(f"{'='*50}\n<ansicyan>[A]</ansicyan> Adicionar comando customizado\n<ansired>[B]</ansired> Voltar\n<ansiyellow>Escolha uma opção:</ansiyellow> "))
            if choice.lower() == 'a':
                await add_custom_command_to_queue()
            elif choice.lower() == 'b':
                clear_terminal()
                return
            else:
                ""


async def remove_command_from_queue():
    try:
        idx = int(await session.prompt_async(HTML("<ansiyellow>Digite o índice do comando a ser removido:</ansiyellow> ")))
        if 1 <= idx <= len(command_queue):
            removed_command = command_queue.pop(idx - 1)
            print(f"{Fore.GREEN}Comando {Fore.RED}removido{Fore.GREEN}: {removed_command['command']}")
        else:
            print(f"{Fore.RED}Índice fora do intervalo.")
    except ValueError:
        print(f"{Fore.RED}Entrada inválida. Por favor, insira um número válido.")


async def add_custom_command_to_queue():
    custom_command = await session.prompt_async(HTML("<ansiyellow>Digite o comando customizado:</ansiyellow> "))
    command_data = {
        "tool": "custom",
        "mode": "custom",
        "command": custom_command
    }
    command_queue.append(command_data)
    print(f"Comando customizado adicionado: {custom_command}")



async def get_scan_technique():
    clear_terminal()
    print(f"""
    {Fore.CYAN}[1] {Fore.RESET}-sS (TCP SYN Scan)
    {Fore.CYAN}[2] {Fore.RESET}-sT (TCP Connect Scan)
    {Fore.CYAN}[3] {Fore.RESET}-sU (UDP Scan)
    {Fore.CYAN}[4] {Fore.RESET}-sF (TCP FIN Scan)
    {Fore.CYAN}[5] {Fore.RESET}-sN (TCP NULL Scan)
    {Fore.CYAN}[6] {Fore.RESET}-sX (TCP Xmas Scan)
    {Fore.CYAN}[7] {Fore.RESET}Todas as técnicas (-sS, -sT, -sU, -sF, -sN, -sX)
    """)
    
    choice = await session.prompt_async(HTML(f"<ansigreen>Escolha uma técnica ou</ansigreen> <ansired>[B]</ansired><ansigreen> para voltar:</ansigreen> "))
    
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
        return await get_scan_technique() 
