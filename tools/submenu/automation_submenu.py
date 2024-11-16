# Bibliotecas e Dependências:
import asyncio
import os
from prompt_toolkit import PromptSession
from colorama import Fore, Style, init
from functions.clear_terminal import clear_terminal
from functions.set_global_target import state
from functions.create_output_file import execute_command_and_log_submenu
from prompt_toolkit.formatted_text import HTML
from configurations.ar_updater import new_version_checker

# Inicialização e Configurações:
init(autoreset=True)
session = PromptSession()
is_running = False
automation_lock = asyncio.Lock()

# Variáveis Globais:
command_queue = []
stop_event = asyncio.Event()

# Estruturas de Comandos:

#TODO Adicionar na biblioteca a lista de comandos para cada ferramenta

#TODO Adicionar menu para outras ferramentas

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
    },

    "nuclei": {
        "target_spec": {
            "command": "sudo nuclei",
            "params": lambda target: f"-target {target}"
        },
        "severity": {
            "command": "sudo nuclei",
            "params": lambda target, severity: f"-severity {severity} -target {target}",
            "all": ['low', 'medium', 'high', 'critical']
        },
        "multi_target": {
            "command": "sudo nuclei",
            "params": lambda target_file: f"-targets {target_file}"
        },
        "network_scan": {
            "command": "sudo nuclei",
            "params": lambda target: f"-target {target}"
        },
        "custom_template": {
            "command": "sudo nuclei",
            "params": lambda url, template: f"-u {url} -t {template}"
        },
        "dashboard": {
            "command": "sudo nuclei",
            "params": lambda target: f"-target {target} -dashboard"
        }
    }
}


# Funções de Formatação e Adição de Comandos:
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
        elif mode == "severity":
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

# Funções de Execução:
def stop_execution():
    stop_event.set()

async def execute_commands_in_intervals(interval_minutes):
    global is_running
    is_running = True

    try:
        while is_running:
            for command_data in command_queue:
                if stop_event.is_set():
                    is_running = False
                    break
                await process_command(command_data)
            
            if not is_running:
                break
            
            print(f"{Fore.CYAN}Iniciando automação com intervalos de {interval_minutes} minutos\nPressione {Fore.RED}Enter{Fore.CYAN} para interromper a execução.\n{Fore.YELLOW}Aguardando {interval_minutes} minutos para a próxima execução...{Fore.RESET}\n")
            await asyncio.wait([asyncio.create_task(stop_event.wait()), asyncio.create_task(asyncio.sleep(interval_minutes * 60))], return_when=asyncio.FIRST_COMPLETED)
            if stop_event.is_set():
                is_running = False
                break

    except asyncio.CancelledError:
        print("\nAutomação interrompida pelo usuário.\nVoltando para o Submenu...")
    finally:
        stop_event.clear()

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

async def edit_queue_menu():
    while True:
        clear_terminal()
        update_message = (
            f"{Fore.RED}Outdated{Fore.YELLOW} - @LuizWt {Fore.RED}\n"
            f"Utilize 'sudo autorecon -update' para atualizar"
            if new_version_checker()
            else f"{Fore.GREEN}Latest{Fore.YELLOW} - @LuizWt"
        )
        global_target_display = (
            f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"
        )

        print(rf"""
            {Fore.BLUE}{Style.BRIGHT}
           _____     _____      _              _       _  {Fore.GREEN}Edição de Queue{Fore.BLUE}{Style.BRIGHT}         
     /\   |  __ \   / ____|    | |            | |     | |  {Fore.YELLOW}{global_target_display}{Fore.BLUE}        
    /  \  | |__) | | (___   ___| |__   ___  __| |_   _| | ___ _ __ 
   / /\ \ |  _  /   \___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \ '__|
  / ____ \| | \ \   ____) | (__| | | |  __/ (_| | |_| | |  __/ |   
 /_/    \_\_|  \_\ |_____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|   

 {Fore.YELLOW}+ -- --=[ https://github.com/LuizWT/
 {Fore.YELLOW}+ -- --=[ AutoRecon v1.3.0 {update_message}
        """)

        if command_queue:
            print(f"{Fore.CYAN}Comandos na Fila de Automação:{Style.RESET_ALL}")
            for idx, cmd in enumerate(command_queue, start=1):
                print(f"{Fore.CYAN}[{idx}]{Fore.RESET} {cmd['command']}")

            print(f"\n{'_' * 30}\n\n{Fore.CYAN}[A]{Fore.RESET} Adicionar comando customizado\n{Fore.CYAN}[E]{Fore.RESET} Editar um comando\n{Fore.RED}[R]{Fore.RESET} Remover um comando\n{Fore.RED}[B]{Fore.RESET} Voltar\n")

            
            choice = await session.prompt_async(
                HTML("<ansiyellow>Escolha uma opção:</ansiyellow> ")
            )
            if choice.lower() == 'r':
                await remove_command_from_queue()
            elif choice.lower() == 'a':
                await add_custom_command_to_queue()
            elif choice.lower() == 'e':
                await edit_command_in_queue()
            elif choice.lower() == 'b':
                clear_terminal()
                return
            else:
                pass
        else:
            print(f"{Fore.YELLOW}A fila de comandos está vazia.{Style.RESET_ALL}")
            print(f"\n{'_' * 30}\n\n{Fore.CYAN}[A]{Fore.RESET} Adicionar comando customizado\n{Fore.RED}[B]{Fore.RESET} Voltar\n")

            choice = await session.prompt_async(
                HTML("<ansiyellow>Escolha uma opção:</ansiyellow> ")
            )
            if choice.lower() == 'a':
                await add_custom_command_to_queue()
            elif choice.lower() == 'b':
                clear_terminal()
                return
            else:
                pass

async def remove_command_from_queue():

    idx_input = await session.prompt_async(HTML("<ansiyellow>Digite o índice do comando a ser removido:</ansiyellow> "))
    
    try:
        idx = int(idx_input)
        if 1 <= idx <= len(command_queue):
            command_queue.pop(idx - 1)
        else:
            print(f"{Fore.RED}Índice fora do intervalo.")
    except ValueError:
        print(f"{Fore.RED}Entrada inválida. Por favor, insira um número válido.")


async def edit_command_in_queue():
    try:
        index = int(await session.prompt_async(HTML("<ansiyellow>Informe o número do comando para editar:</ansiyellow> "))) - 1
        if 0 <= index < len(command_queue):
            command = command_queue[index]
            old_command = command['command']
            clear_terminal()
            print(f"{Fore.CYAN}Comando atual: {old_command}{Style.RESET_ALL}")

            # Permite editar o comando na linha completa
            edited_command = await session.prompt_async(HTML(f"<ansiyellow>Edite o comando (ou deixe em branco para manter o atual): </ansiyellow> "), default=old_command)
            
            # Se o usuário pressionar Enter sem digitar nada, mantém o comando original
            if edited_command.strip() == "":
                print(f"{Fore.YELLOW}Comando mantido: {old_command}{Style.RESET_ALL}")
            else:
                command_queue[index]['command'] = edited_command.strip()
        else:
            print(f"{Fore.RED}Índice inválido. Tente novamente.{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Entrada inválida. Tente novamente.{Style.RESET_ALL}")


async def add_custom_command_to_queue():
    custom_command = await session.prompt_async(HTML("<ansiyellow>Digite o comando customizado:</ansiyellow> "))
    command_data = {
        "tool": "custom",
        "mode": "custom",
        "command": custom_command
    }
    command_queue.append(command_data)



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
    


# MENUS:

async def nuclei_menu():
    target = state['global_target']
    global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"
    while True:

        print(rf"""{Fore.BLUE}
         _   _            _      _ {Fore.YELLOW}{global_target_display}{Fore.BLUE}
        | \ | |          | |    (_) 
        |  \| |_   _  ___| | ___ _ 
        | . ` | | | |/ __| |/ _ \ |
        | |\  | |_| | (__| |  __/ |
        |_| \_|\__,_|\___|_|\___|_|
                                    
        {Fore.CYAN}[1] {Fore.RESET}Varredura padrão 
        {Fore.CYAN}[2] {Fore.RESET}Filtrar por severidade
        {Fore.CYAN}[3] {Fore.RESET}Varredura múltipla
        {Fore.CYAN}[4] {Fore.RESET}Varredura de rede
        {Fore.CYAN}[5] {Fore.RESET}Usar template personalizado
        {Fore.CYAN}[6] {Fore.RESET}Enviar para ProjectDiscovery
        {Fore.RED}[B] {Fore.RESET}Voltar
        """)

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "))

        if option == '1':
            add_command_to_queue("nuclei", "target_spec", target)
        elif option == '2':
            while True:
                severity = await session.prompt_async(HTML("<ansiyellow>Digite a severidade (low, medium, high, critical) ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if severity.lower() == 'b':
                    clear_terminal()
                    break
                elif severity.lower() in ['low','medium', 'high', 'critical']:
                    add_command_to_queue("nuclei", "severity", target, severity)
                else:
                    print(f"{Fore.RED}Entrada inválida. Por favor, forneça uma severidade (low, medium, high, critical) ou [B] para voltar.")
        elif option == '3':
            while True:
                target = await session.prompt_async(HTML(f"<ansiyellow>Digite o caminho para o arquivo com a lista de alvos ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if target.lower() == 'b':
                    clear_terminal()
                    continue
                if os.path.isfile(target):
                    add_command_to_queue("nuclei", "multi_target", target)
                    print(f"{Fore.GREEN}Arquivo encontrado:{Fore.RESET} {target}")
                    break
                else:
                    print(f"{Fore.RED}Arquivo não encontrado. Tente novamente.")
        elif option == '4':
            add_command_to_queue("nuclei", "network_scan", target)
        elif option == '5':
            template = await session.prompt_async(HTML("<ansiyellow>Digite a URL e o template separados por espaço:</ansiyellow> "))
            if template.lower() == 'b':
                clear_terminal()
                continue
            template_data = template.split()
            if len(template_data) == 2:
                add_command_to_queue("nuclei", "custom_template", template_data)
            else:
                print(f"{Fore.RED}Entrada inválida. Por favor, forneça uma URL e um template separados.")
        elif option == '6':
            add_command_to_queue("nuclei", "dashboard", target)
        elif option.lower() == 'b':
            clear_terminal()
            return
        else:
            clear_terminal()



async def nmap_menu():
    target = state['global_target']
    global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"
    while True:
        print(rf"""
        {Fore.BLUE}                  
        _ __  _ __ ___   __ _ _ __  
        | '_ \| '_ ` _ \ / _` | '_ \      {Fore.YELLOW}{global_target_display}{Fore.BLUE}
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

async def automation_setup_menu():
    if new_version_checker():
        update_message = f"{Fore.RED}Outdated{Fore.YELLOW} - @LuizWt {Fore.RED}\nUtilize 'sudo autorecon -update' para atualizar"
    else:
        update_message = f"{Fore.GREEN}Latest{Fore.YELLOW} - @LuizWt"
    global is_running
    global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"
    while True:
        print(rf"""
            {Fore.BLUE}{Style.BRIGHT}
           _____     _____      _              _       _  {Fore.GREEN}Configuração de Automação{Fore.BLUE}{Style.BRIGHT}         
     /\   |  __ \   / ____|    | |            | |     | |  {Fore.YELLOW}{global_target_display}{Fore.BLUE}        
    /  \  | |__) | | (___   ___| |__   ___  __| |_   _| | ___ _ __ 
   / /\ \ |  _  /   \___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \ '__|
  / ____ \| | \ \   ____) | (__| | | |  __/ (_| | |_| | |  __/ |   
 /_/    \_\_|  \_\ |_____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|   

 {Fore.YELLOW}+ -- --=[ https://github.com/LuizWT/
 {Fore.YELLOW}+ -- --=[ AutoRecon v1.3.0 {update_message}    
        
    {Fore.YELLOW}Escolha uma ferramenta para adicionar comandos à fila de automação:
    {Fore.CYAN}[1]{Fore.RESET} NMAP
    {Fore.CYAN}[2]{Fore.RESET} NUCLEI
    {Fore.CYAN}[A]{Fore.RESET} Iniciar Automação
    {Fore.CYAN}[Q]{Fore.RESET} Editar Queue
    {Fore.RED}[B]{Fore.RESET} Sair""")

        choice = await session.prompt_async(HTML("\n<ansiyellow>Escolha uma opção:</ansiyellow> "))

        if choice == '1':
            clear_terminal()
            await nmap_menu()
        if choice == '2':
            clear_terminal()
            await nuclei_menu()
        
        elif choice.lower() == 'a':
            while True:
                interval_input = await session.prompt_async(HTML("<ansiyellow>Digite o intervalo (em minutos) ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if interval_input.lower() == 'b':
                    clear_terminal()
                    break
                try:
                    interval = int(interval_input)
                    if interval > 0:
                        asyncio.create_task(execute_commands_in_intervals(interval))
                        await session.prompt_async("")
                        stop_execution()
                    else:
                        print("Por favor, insira um número inteiro positivo.")
                    if not await execute_commands_in_intervals(interval):
                        clear_terminal()
                        break
                except ValueError:
                    print(f"{Fore.RED}Entrada inválida. Por favor, insira um número inteiro.")
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
