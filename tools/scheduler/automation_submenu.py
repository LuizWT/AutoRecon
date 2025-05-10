# Bibliotecas e Dependências:
import asyncio
import os
import json
from threading import Event
from pathlib import Path
from prompt_toolkit import PromptSession
from colorama import Fore, Style, init
from functions.clear_terminal import clear_terminal
from functions.set_global_target import global_target
from functions.validations.validate_protocol import validate_url
from functions.validations.is_valid import is_valid_cidr
from functions.create_output_file import execute_command_and_log_submenu
from functions.validations.validate_ports import validate_ports
from prompt_toolkit.formatted_text import HTML
from configurations.ar_updater import new_version_checker
from configurations.version import __version__

# Inicialização e Configurações:
init(autoreset=True)
session = PromptSession()
is_running = False
automation_lock = asyncio.Lock()

# Variáveis Globais:
stop_event = asyncio.Event()

# Caminho fixo para o armazenamento dos comandos
BASE_DIR    = Path(__file__).resolve().parent
QUEUE_DIR   = BASE_DIR / "storage"
QUEUE_FILE  = QUEUE_DIR / "commands_queue.txt"

# Estruturas de Comandos:
#TODO Adicionar na biblioteca a lista de comandos para cada ferramenta
#TODO Adicionar menu para outras ferramentas
tools_commands = {
    "nmap": {
        "target_spec": {
            "command": "sudo nmap",
            "params": lambda target: f"{target}"
        },
        "scan_technique": {
            "command": "sudo nmap",
            "params": lambda technique, target: f"{technique} {target}",
            "all": ['-sS', '-sT', '-sU', '-sF', '-sN', '-sX'],
        },
        "host_discovery": {
            "command": "sudo nmap",
            "params": lambda target: f"-sn {target}"
        },
        "port_spec": {
            "command": "sudo nmap",
            "params": lambda target, port: f"-p {port} {target}"
        },
        "service_detection": {
            "command": "sudo nmap",
            "params": lambda target: f"-sV {target}"
        },
        "os_detection": {
            "command": "sudo nmap",
            "params": lambda target: f"-O {target}"
        },
        "timing": {
            "command": "sudo nmap",
            "params": lambda target, level: f"-T {level} {target}"
        },
        "http_title": {
            "command": "sudo nmap",
            "params": lambda target: f"-p 80,443 --script=http-title {target}"
        },
        "ssl_cert": {
            "command": "sudo nmap",
            "params": lambda target: f"-p 443 --script=ssl-cert {target}"
        },
        "vuln": {
            "command": "sudo nmap",
            "params": lambda target: f"-p 80,443 --script=vuln {target}"
        },
        "smb_os_discovery": {
            "command": "sudo nmap",
            "params": lambda target: f"-p 445 --script=smb-os-discovery {target}"
        },
        "http_robots_txt": {
            "command": "sudo nmap",
            "params": lambda target: f"-p 80,443 --script=http-robots.txt {target}"
        },
        "ssh_hostkey": {
            "command": "sudo nmap",
            "params": lambda target: f"-p 22 --script=ssh-hostkey {target}"
        },
        "dns_brute": {
            "command": "sudo nmap",
            "params": lambda target: f"--script=dns-brute --script-args dns-brute.domain={target}"
        },
        "all_commands": {
            "command": "sudo nmap",
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
    },

    "sniper": {
        "normal": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target}"
        },
        "osint_recon": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target} -o -re"
        },
        "stealth": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target} -m stealth -o -re"
        },
        "discover": {
            "command": "sudo sniper",
            "params": lambda target, wordlist: f"-t {target} -m discover -w {wordlist}"
        },
        "port": {
            "command": "sudo sniper",
            "params": lambda target, ports: f"-t {target} -m port -p {ports}"
        },
        "fullportonly": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target} -fp"
        },
        "web": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target} -m web"
        },
        "webporthttp": {
            "command": "sudo sniper",
            "params": lambda target, ports: f"-t {target} -m webporthttp -p {ports}"
        },
        "webporthttps": {
            "command": "sudo sniper",
            "params": lambda target, ports: f"-t {target} -m webporthttps -p {ports}"
        },
        "webscan": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target} -m webscan"
        },
        "bruteforce": {
            "command": "sudo sniper",
            "params": lambda target: f"-t {target} -b"
        }
    },

    "nikto": {
        "vuln_checks": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -C all"
        },
        "server_modules": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -M all"
        },
        "config_files": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -e all"
        },
        "cookie_security": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -C -p"
        },
        "protocols": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -p"
        },
        "dir_file_scan": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -d"
        },
        "third_party_scripts": {
            "command": "sudo nikto",
            "params": lambda target: f"-h {target} -T"
        },
        "all_commands": {
            "command": "sudo nikto",
            "params": lambda target: [
                f"-h {target} -C all",     # Vulnerability checks
                f"-h {target} -M all",     # Server modules checks
                f"-h {target} -e all",     # Configuration files tests
                f"-h {target} -C -p",      # Cookie security
                f"-h {target} -p",         # Protocols checks
                f"-h {target} -d",         # Directory and file scan
                f"-h {target} -T"          # Third-party scripts checks
            ]
        }
    },

    "wpscan": {
        "normal": {
            "command": "sudo wpscan",
            "params": lambda target: f"--url {target}"
        },
        "enumerate_users": {
            "command": "sudo wpscan",
            "params": lambda target: f"--url {target} --enumerate u"
        },
        "enumerate_plugins": {
            "command": "sudo wpscan",
            "params": lambda target: f"--url {target} --enumerate p"
        },
        "enumerate_themes": {
            "command": "sudo wpscan",
            "params": lambda target: f"--url {target} --enumerate t"
        },
        "scan": {
            "command": "sudo wpscan",
            "params": lambda target, api_token: f"--url {target} --api-token {api_token}"
        }
    }
}


# Funções de Execução:
async def wait_for_enter():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, input)

    stop_event.set()

def stop_execution():
    stop_event.set()

# Funções de Formatação e Adição de Comandos:
def format_command(tool, mode, target, additional_param=None):
    if mode in tools_commands[tool]:
        command = tools_commands[tool][mode]['command']
        params_function = tools_commands[tool][mode]['params']

        # Modos que precisam de additional_param antes do target
        if mode in {"scan_technique", "port_spec", "timing", "severity"}:
            if additional_param is None:
                raise ValueError(f"O modo '{mode}' requer um parâmetro adicional.")
            return f"{command} {params_function(additional_param, target)}"

        elif mode in {"host_discovery"}:
            return f"{command} {params_function(target)}"

        elif mode == "all_commands":
            commands = params_function(target)
            return "\n".join([f"{command} {cmd}" for cmd in commands])

        # Modos padrão (target e additional_param (se fornecido))
        else:
            if additional_param:
                return f"{command} {params_function(target, additional_param)}"
            return f"{command} {params_function(target)}"

    # Comando genérico caso nada seja definido
    return f"{tool} {target}"

# Cria o diretório e arquivo, se necessário
def ensure_queue_file():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        QUEUE_FILE.write_text("")

# Carrega os comandos do arquivo
def load_command_queue():
    ensure_queue_file()
    lines = QUEUE_FILE.read_text().strip().splitlines()
    return [json.loads(line) for line in lines if line.strip()]

# Salva a fila inteira (sobrescreve)
def save_command_queue(queue):
    ensure_queue_file()
    with QUEUE_FILE.open("w") as f:
        for command in queue:
            f.write(json.dumps(command) + "\n")

# Adiciona um novo comando ao arquivo (storage/commands_queue.txt)
def add_command_to_queue(tool_name, mode, target, additional_param=None):
    from tools.scheduler.automation_submenu import format_command, clear_terminal

    formatted_command = format_command(tool_name, mode, target, additional_param)
    commands_added = []

    queue = load_command_queue()

    if mode == "all_commands":
        commands = formatted_command.split('\n')
        for cmd in commands:
            command_data = {
                "tool": tool_name,
                "mode": mode,
                "command": cmd.strip()
            }
            queue.append(command_data)
            commands_added.append(cmd.strip())
    else:
        command_data = {
            "tool": tool_name,
            "mode": mode,
            "command": formatted_command
        }
        queue.append(command_data)
        commands_added.append(formatted_command)

    save_command_queue(queue)

    clear_terminal()
    print(f"{Fore.GREEN}Comandos adicionados:\n" + "\n".join(commands_added))

# Remove comando pelo índice
def remove_command_by_index(index):
    queue = load_command_queue()
    if 0 <= index < len(queue):
        queue.pop(index)
        save_command_queue(queue)

# Limpa todos os comandos
def clear_command_queue():
    save_command_queue([])

# Edita um comando específico
def edit_command(index, new_command):
    queue = load_command_queue()
    if 0 <= index < len(queue):
        queue[index]["command"] = new_command
        save_command_queue(queue)

# Lista os comandos (formatados)
def get_formatted_command_list():
    queue = load_command_queue()
    return [f"{Fore.CYAN}[{i + 1}]{Fore.RESET} {cmd['command']}" for i, cmd in enumerate(queue)]

# Aplica proxychains aos comandos escolhidos via índice
async def apply_proxychains_to_command():
    queue = load_command_queue()

    if not queue:
        print(f"{Fore.YELLOW}[INFO] A fila de comandos está vazia. Nada a aplicar.{Style.RESET_ALL}")
        return

    try:
        while True:
            print(f"{Fore.CYAN}Comandos na Fila de Automação:{Style.RESET_ALL}")
            formatted_commands = get_formatted_command_list()
            print("\n".join(formatted_commands))

            user_input = await session.prompt_async(
                HTML("<ansiyellow>Digite o índice do comando (ou use números separados por vírgula)</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> ")
            )
            if user_input.lower() == 'b':
                break

            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]

                for index in indices:
                    if 0 <= index < len(queue):
                        command = queue[index]['command']

                        if command.startswith("proxychains ") or command.startswith("proxychains4 "):
                            clear_terminal()
                            print(f"{Fore.YELLOW}[INFO] O comando '{command}' já está configurado com ProxyChains.{Style.RESET_ALL}\n")
                        elif command.startswith("sudo "):
                            if not command.startswith("sudo proxychains "):
                                new_command = command.replace("sudo ", "sudo proxychains ", 1)
                                queue[index]['command'] = new_command
                                clear_terminal()
                                print(f"{Fore.GREEN}[INFO] {command} -> {new_command}{Style.RESET_ALL}\n")
                            else:
                                clear_terminal()
                                print(f"{Fore.YELLOW}[INFO] O comando '{command}' já está configurado com ProxyChains.{Style.RESET_ALL}\n")
                        else:
                            new_command = f"proxychains {command}"
                            queue[index]['command'] = new_command
                            clear_terminal()
                            print(f"{Fore.GREEN}[INFO] {command} -> {new_command}{Style.RESET_ALL}\n")
                    else:
                        clear_terminal()
                        print(f"{Fore.RED}[ERROR] Índice inválido: {index + 1}. Ignorado.{Style.RESET_ALL}\n")

                save_command_queue(queue)

            except ValueError:
                clear_terminal()
                print(f"{Fore.RED}[ERROR] Entrada inválida. Tente novamente com índices válidos, separados por vírgulas.{Style.RESET_ALL}\n")

    except ValueError:
        clear_terminal()
        print(f"{Fore.RED}[ERROR] Entrada inválida. Tente novamente.{Style.RESET_ALL}")

async def execute_commands_in_intervals(interval_minutes):
    is_running = True

    # Cria uma tarefa para aguardar o Enter
    enter_task = asyncio.create_task(wait_for_enter())

    try:
        while is_running:
            queue = load_command_queue()
            for command_data in queue:
                if stop_event.is_set():  # Verifica se o usuário solicitou parada
                    is_running = False
                    break
                await process_command(command_data)

            if not is_running:
                break

            print(
                f"{Fore.CYAN}Iniciando automação com intervalos de {interval_minutes} minutos"
                f"\nPressione {Fore.RED}Enter (x2){Fore.CYAN} para interromper a execução."
                f"\n{Fore.YELLOW}Aguardando {interval_minutes} minutos para a próxima execução...{Fore.RESET}\n"
            )

            # Cria explicitamente uma Task para o sleep (asyncio.wait não aceita coroutines)
            sleep_task = asyncio.create_task(asyncio.sleep(interval_minutes * 60))
            # Aguarda um Enter ou o sleep
            done, pending = await asyncio.wait(
                [enter_task, sleep_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Se Enter = True, para e cancela o sleep
            if enter_task in done:
                is_running = False
                # Cancela o sleep caso ainda esteja pendente (certa precaução)
                if not sleep_task.done():
                    sleep_task.cancel()
                break

            # Se sleep = True, continua o loop e recria o sleep na próxima iteração
            if sleep_task in done:
                # Reinicia a tarefa de Enter para a próxima iteração
                enter_task = asyncio.create_task(wait_for_enter())

    except asyncio.CancelledError:
        print("\nAutomação interrompida pelo usuário.\nVoltando para o Submenu...")
    finally:
        # Reseta o evento para permitir futuras execuções -- Essa função só me da trabalho, não aguento mais
        stop_event.clear()


async def process_command(command_data):
    # Executa um comando da fila usando EXATAMENTE a string que foi salva em command_data['command'],

    tool = command_data.get("tool")
    cmd_str = command_data.get("command")

    try:
        await execute_command_and_log_submenu(cmd_str, tool)
    except Exception as e:
        print(f"[ERRO] Falha ao executar '{cmd_str}': {e}")

async def edit_queue_menu(session, new_version_checker):
    while True:
        clear_terminal()
        update_message = (
            f"{Fore.RED}Outdated{Fore.YELLOW} - @LuizWt {Fore.RED}\nUtilize 'sudo autorecon -update' para atualizar"
            if new_version_checker() else f"{Fore.GREEN}Latest{Fore.YELLOW} - @LuizWt"
        )
        global_target_display = (
            f"Alvo: {global_target.value}" if global_target.value else "Alvo: Não definido"
        )

        print(rf"""
            {Fore.BLUE}
           _____     _____      _              _       _  {Fore.GREEN}Edição de Queue{Fore.BLUE}         
     /\   |  __ \   / ____|    | |            | |     | |  {Fore.YELLOW}{global_target_display}{Fore.BLUE}        
    /  \  | |__) | | (___   ___| |__   ___  __| |_   _| | ___ _ __ 
   / /\ \ |  _  /   \___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \ '__|
  / ____ \| | \ \   ____) | (__| | | |  __/ (_| | |_| | |  __/ |   
 /_/    \_\_|  \_\ |_____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|   

 {Fore.YELLOW}+ -- --=[ https://github.com/LuizWT/
 {Fore.YELLOW}+ -- --=[ AutoRecon {update_message}
        """)

        queue = load_command_queue()

        if queue:
            print(f"{Fore.CYAN}Comandos na Fila de Automação:{Fore.RESET}")
            formatted_commands = get_formatted_command_list()
            print("\n".join(formatted_commands))

            print(f"\n{'_' * 30}\n\n{Fore.CYAN}[A]{Fore.RESET} Adicionar comando customizado\n{Fore.CYAN}[E]{Fore.RESET} Editar um comando\n{Fore.CYAN}[P]{Fore.RESET} Aplicar Proxychains\n{Fore.RED}[R]{Fore.RESET} Remover um comando\n{Fore.RED}[RA]{Fore.RESET} Remover todos os comandos\n{Fore.RED}[B]{Fore.RESET} Voltar\n")

            choice = await session.prompt_async(HTML("<ansiyellow>Escolha uma opção:</ansiyellow> "))
            if choice.lower() == 'r':
                await remove_command_from_queue(session)
            elif choice.lower() == 'ra':
                while True:
                    confirm = await session.prompt_async(HTML("<ansiyellow>Tem certeza que deseja remover todos os comandos da fila? (y/n):</ansiyellow> "))
                    if confirm.lower() in ['s', 'y']:
                        clear_command_queue()
                        break
                    elif confirm.lower() == 'n':
                        break
                    else:
                        print(f"{Fore.RED}[ERROR] Digite um valor válido (y/n)")
            elif choice.lower() == 'a':
                await add_custom_command_to_queue(session)
            elif choice.lower() == 'e':
                await edit_command_in_queue(session)
            elif choice.lower() == 'p':
                from tools.scheduler.automation_submenu import apply_proxychains_to_command
                clear_terminal()
                await apply_proxychains_to_command()
            elif choice.lower() == 'b':
                clear_terminal()
                return
        else:
            print(f"{Fore.YELLOW}A fila de comandos está vazia.{Fore.RESET}")
            print(f"\n{'_' * 30}\n\n{Fore.CYAN}[A]{Fore.RESET} Adicionar comando customizado\n{Fore.RED}[B]{Fore.RESET} Voltar\n")

            choice = await session.prompt_async(HTML("<ansiyellow>Escolha uma opção:</ansiyellow> "))
            if choice.lower() == 'a':
                await add_custom_command_to_queue(session)
            elif choice.lower() == 'b':
                clear_terminal()
                return

async def remove_command_from_queue(session):
    queue = load_command_queue()
    idx_input = await session.prompt_async(HTML("<ansiyellow>Digite o índice do comando a ser removido:</ansiyellow> "))
    try:
        idx = int(idx_input)
        if 1 <= idx <= len(queue):
            remove_command_by_index(idx - 1)
        else:
            print(f"{Fore.RED}Índice fora do intervalo.")
    except ValueError:
        print(f"{Fore.RED}Entrada inválida. Por favor, insira um número válido.")

async def edit_command_in_queue(session):
    queue = load_command_queue()
    try:
        index = int(await session.prompt_async(HTML("<ansiyellow>Informe o número do comando para editar:</ansiyellow> "))) - 1
        if 0 <= index < len(queue):
            old_command = queue[index]['command']
            clear_terminal()
            print(f"{Fore.CYAN}Comando atual: {old_command}{Fore.RESET}")

            edited_command = await session.prompt_async(HTML("<ansiyellow>Edite o comando (ou deixe em branco para manter o atual): </ansiyellow> "), default=old_command)

            if edited_command.strip() == "":
                print(f"{Fore.YELLOW}Comando mantido: {old_command}{Fore.RESET}")
            else:
                edit_command(index, edited_command.strip())
        else:
            print(f"{Fore.RED}Índice inválido. Tente novamente.{Fore.RESET}")
    except ValueError:
        print(f"{Fore.RED}Entrada inválida. Tente novamente.{Fore.RESET}")

async def add_custom_command_to_queue(session):
    custom_command = await session.prompt_async(HTML("<ansiyellow>Digite o comando customizado:</ansiyellow> "))
    queue = load_command_queue()
    queue.append({
        "tool": "custom",
        "mode": "custom",
        "command": custom_command
    })
    save_command_queue(queue)

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
    

async def get_network_target_submenu():
    while True:
        target = await session.prompt_async(HTML(f"<ansigreen>Digite o alvo da rede (EX: 192.168.1.0/24) ou</ansigreen> <ansired>[B]</ansired> <ansigreen>para voltar:</ansigreen> "))
        if target.lower() == 'b':
            return None
        if is_valid_cidr(target):
            return target
        else:
            print(f"{Fore.RED}Formato inválido. Por favor, insira um endereço CIDR válido.{Fore.RESET}")

# MENUS:
async def nuclei_menu():
    target = global_target.value
    global_target_display = f"Alvo: {global_target.value}" or "Alvo: Não definido"
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
                    break
                else:
                    print(f"{Fore.RED}Entrada inválida. Por favor, forneça uma severidade (low, medium, high, critical) ou [B] para voltar.")
        elif option == '3':
            while True:
                multiple_target = await session.prompt_async(HTML(f"<ansiyellow>Digite o caminho para o arquivo com a lista de alvos ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if multiple_target.lower() == 'b':
                    clear_terminal()
                    break
                if os.path.isfile(multiple_target):
                    add_command_to_queue("nuclei", "multi_target", multiple_target)
                    print(f"{Fore.GREEN}Arquivo encontrado:{Fore.RESET} {multiple_target}")
                    break
                else:
                    print(f"{Fore.RED}Arquivo não encontrado. Tente novamente.")
        elif option == '4':
            target = await get_network_target_submenu()
            if target is None:
                clear_terminal()
                return
            add_command_to_queue("nuclei", "network_scan", target)
        elif option == '5':
            while True:
                template = await session.prompt_async(HTML("<ansiyellow>Digite a URL e o template separados por espaço ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if template.lower() == 'b':
                    clear_terminal()
                    break
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
    target = global_target.value
    global_target_display = f"Alvo: {global_target.value}" or "Alvo: Não definido"
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

            if technique == 'all':
                techniques = ['-sS', '-sT', '-sU', '-sF', '-sN', '-sX']
                for tech in techniques:
                    add_command_to_queue("nmap", "scan_technique", target, tech)
            else:
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

async def nikto_menu():
    target = global_target.value
    global_target_display = f"Alvo: {global_target.value}" or "Alvo: Não definido"
    clear_terminal()
    while True:
        
        print(rf"""
        {Fore.BLUE}
          _   _ _ _    _        
         | \ | (_) |  | |   Pressione Ctrl+T para definir o alvo
         |  \| |_| | _| |_ ___  {Fore.YELLOW}{global_target_display}{Fore.BLUE}
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

        mode_choice = await session.prompt_async(HTML(f"<ansiyellow>\nEscolha um modo para Nikto:</ansiyellow> "))

        if mode_choice.lower() == 'b':
            break

        if mode_choice == "1":
            add_command_to_queue("nikto", "vuln_checks", target)
        elif mode_choice == "2":
            add_command_to_queue("nikto", "server_modules", target)
        elif mode_choice == "3":
            add_command_to_queue("nikto", "config_files", target)
        elif mode_choice == "4":
            add_command_to_queue("nikto", "cookie_security", target)
        elif mode_choice == "5":
            add_command_to_queue("nikto", "protocols", target)
        elif mode_choice == "6":
            add_command_to_queue("nikto", "dir_file_scan", target)
        elif mode_choice == "7":
            add_command_to_queue("nikto", "third_party_scripts", target)
        elif mode_choice == "8":
            add_command_to_queue("nikto", "all_commands", target)
        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida. Tente novamente.")
            await asyncio.sleep(2)

async def wpscan_menu():
    target = global_target.value
    target = validate_url(target)
    global_target_display = f"Alvo: {target}" if target else "Alvo: Não definido"
    clear_terminal()
    while True:
        
        print(rf"""
        {Fore.BLUE}
        __          _______   _____  _____          _   _ Pressione Ctrl+T para definir o alvo
        \ \        / /  __ \ / ____|/ ____|   /\   | \ | |       {Fore.YELLOW}{global_target_display}{Fore.BLUE}
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

        mode_choice = await session.prompt_async(HTML(f"<ansiyellow>\nEscolha um modo para WPSCAN:</ansiyellow> "))

        if mode_choice.lower() == 'b':
            break

        if not target:
            print(f"{Fore.RED}Nenhum alvo definido. Pressione Ctrl+T para configurar um.")
            await asyncio.sleep(2)
            continue

        if mode_choice == "1":
            add_command_to_queue("wpscan", "normal", target)
        elif mode_choice == "2":
            add_command_to_queue("wpscan", "enumerate_users", target)
        elif mode_choice == "3":
            add_command_to_queue("wpscan", "enumerate_plugins", target)
        elif mode_choice == "4":
            add_command_to_queue("wpscan", "enumerate_themes", target)
        elif mode_choice == "5":
            while True:
                api_token = await session.prompt_async(HTML("<ansiyellow>Digite seu API Token para WPSCAN ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))

                if api_token.lower() == 'b':
                    clear_terminal()
                    break

                if not api_token.strip():
                    clear_terminal()
                    print(f"{Fore.RED}API Token inválido. Tente novamente.")
                    continue

                add_command_to_queue("wpscan", "scan", target, api_token)
                break

        else:
            clear_terminal()
            print(f"{Fore.RED}Opção inválida. Tente novamente.")
            await asyncio.sleep(2)

async def sniper_menu():
    target = global_target.value
    global_target_display = f"Alvo: {global_target.value}" or "Alvo: Não definido"
    clear_terminal()
    while True:
        print(rf"""
        {Fore.RED}                  
        _____       _                 
        /  ___|     (_)                
        \ `--. _ __  _ _ __   ___ _ __ 
         `--. \ '_ \| | '_ \ / _ \ '__|
        /\__/ / | | | | |_) |  __/ |   
        \____/|_| |_|_| .__/ \___|_|   {Fore.YELLOW}{global_target_display}{Fore.RED}
                      | |              
                      |_|              
        {Fore.CYAN}[1] {Fore.RESET}MODO PADRÃO
        {Fore.CYAN}[2] {Fore.RESET}MODO OSINT + RECONHECIMENTO
        {Fore.CYAN}[3] {Fore.RESET}MODO FURTIVO + OSINT + RECONHECIMENTO
        {Fore.CYAN}[4] {Fore.RESET}MODO DE DESCOBERTA
        {Fore.CYAN}[5] {Fore.RESET}ESCANEAR APENAS PORTA ESPECÍFICA
        {Fore.CYAN}[6] {Fore.RESET}ESCANEAR TODAS AS PORTAS ABERTAS
        {Fore.CYAN}[7] {Fore.RESET}MODO WEB
        {Fore.CYAN}[8] {Fore.RESET}ESCANEAR PORTA HTTP
        {Fore.CYAN}[9] {Fore.RESET}ESCANEAR PORTA HTTPS
        {Fore.CYAN}[10] {Fore.RESET}ESCANEAR VULNERABILIDADES WEB
        {Fore.CYAN}[11] {Fore.RESET}FORÇA BRUTA
        {Fore.RED}[B] {Fore.RESET}Voltar""")

        mode_choice = await session.prompt_async(HTML(f"<ansiyellow>\nEscolha um modo para Sn1per:</ansiyellow> "))

        if mode_choice == '1':
            add_command_to_queue("sniper", "normal", target)
        elif mode_choice == '2':
            add_command_to_queue("sniper", "osint_recon", target)
        elif mode_choice == '3':
            add_command_to_queue("sniper", "stealth", target)
        elif mode_choice == '4':
            while True:
                wordlist = await session.prompt_async(HTML("<ansiyellow>Digite o caminho para o wordlist ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if wordlist.lower() == 'b':
                    clear_terminal()
                    break
                if not os.path.isfile(wordlist):
                    clear_terminal
                    print(f"{Fore.RED}Arquivo não encontrado. Tente novamente.")
                    continue
                add_command_to_queue("sniper", "discover", target, wordlist)
        elif mode_choice == '5':
            while True:
                ports = await session.prompt_async(HTML("<ansiyellow>Digite o número da porta ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if ports.lower() == 'b':
                    clear_terminal()
                    continue
                if not validate_ports(ports):
                    print("[ERROR] Porta inválida (1-65536).")
                    continue
                add_command_to_queue("sniper", "port", target, ports)
                break
        elif mode_choice == '6':
            add_command_to_queue("sniper", "fullportonly", target)
        elif mode_choice == '7':
            add_command_to_queue("sniper", "web", target)
        elif mode_choice == '8':
            while True:
                ports = await session.prompt_async(HTML("<ansiyellow>Digite o número da porta ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if ports.lower() == 'b':
                    clear_terminal()
                    break
                if not validate_ports(ports):
                    print("Portas inválidas! Insira números de 1 a 65535 separados por vírgulas.")
                    continue
                add_command_to_queue("sniper", "webporthttp", target, ports)
                break
        elif mode_choice == '9':
            while True:
                ports = await session.prompt_async(HTML("<ansiyellow>Digite o número da porta ou</ansiyellow> <ansired>[B]</ansired> <ansiyellow>para voltar:</ansiyellow> "))
                if ports.lower() == 'b':
                    clear_terminal()
                    break
                if not validate_ports(ports):
                    print("[ERROR] Porta inválida (1-65536).")
                    continue
                add_command_to_queue("sniper", "webporthttps", target, ports)
                break
        elif mode_choice == '10':
            add_command_to_queue("sniper", "webscan", target)
        elif mode_choice == '11':
            add_command_to_queue("sniper", "bruteforce", target)
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
    global_target_display = (
        f"Alvo: {Fore.GREEN}{global_target.value}{Fore.RESET}"
        if global_target.value
        else f"Alvo: {Fore.RED}Não definido{Fore.RESET}"
    )
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
 {Fore.YELLOW}+ -- --=[ AutoRecon {__version__} {update_message}    
        
    {Fore.YELLOW}Escolha uma ferramenta para adicionar comandos à fila de automação:
    {Fore.CYAN}[1] {Fore.RESET}SNIPER
    {Fore.CYAN}[2] {Fore.RESET}NMAP
    {Fore.CYAN}[3] {Fore.RESET}WPSCAN
    {Fore.CYAN}[4] {Fore.RESET}NUCLEI
    {Fore.CYAN}[5] {Fore.RESET}NIKTO
    {Fore.CYAN}[A]{Fore.RESET} Iniciar Automação
    {Fore.CYAN}[Q]{Fore.RESET} Editar Queue
    {Fore.RED}[B]{Fore.RESET} Sair""")

        choice = await session.prompt_async(HTML("\n<ansiyellow>Escolha uma opção:</ansiyellow> "))

        if choice == '1':
            clear_terminal()
            await sniper_menu()
        if choice == '2':
            clear_terminal()
            await nmap_menu()
        if choice == '3':
            clear_terminal()
            await wpscan_menu()
        if choice == '4':
            clear_terminal()
            await nuclei_menu()
        if choice == '5':
            clear_terminal()
            await nikto_menu()
            
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
            await edit_queue_menu(session, new_version_checker, global_target.value)
        elif choice.lower() == 'b':
            if is_running:
                print(f"{Fore.YELLOW}Automação em andamento. Conclua ou interrompa a execução antes de sair.{Fore.RESET}")
            else:
                clear_terminal()
                print(f"{Fore.GREEN}Saindo da configuração de automação...\nPressione {Fore.RED}Enter{Fore.GREEN} para continuar.")
                return
                
        else:
            clear_terminal()
