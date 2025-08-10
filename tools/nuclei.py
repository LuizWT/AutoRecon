from colorama import init, Fore
from functions.clear_terminal import clear_terminal
from functions.runner import run_command
from functions.logger import get_logger
from functions.proxy_chains import ProxyManager
from functions.validations.is_valid import is_valid_cidr
from functions.set_global_target import set_global_target, global_target
from functions.toggle_info import toggle_info, is_info_visible
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
import asyncio

init(autoreset=True)  # inicia o colorama

logger = get_logger(__name__)
session = PromptSession()
bindings = KeyBindings()

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())

def get_command_explanation(mode):
    explanations = {
        'target_spec': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varredura padrão: Varre um único alvo, IPs, intervalos ou CIDR.",
        'severity': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Severidade: Filtrar os resultados por severidade.",
        'multi_target': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varredura múltipla: Varre uma lista de alvos de um arquivo.",
        'network_scan': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Varredura de rede: Varre uma sub-rede inteira.",
        'custom_template': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Usar template personalizado: Execute um template específico no alvo.",
        'dashboard': f"{Fore.CYAN}| [INFO] {Fore.BLUE}Enviar resultados para o ProjectDiscovery.",
    }
    
    return explanations.get(mode, f"{Fore.RED}| [INFO] Modo não identificado.")

async def nuclei(target, mode, additional_param=None):
    base_command = "nuclei " if not ProxyManager.is_enabled() else "proxychains nuclei "
    command = None

    if mode == 'target_spec':
        command = f"{base_command}-target {target}"
    elif mode == 'severity':
        command = f"{base_command}-severity {additional_param} -target {target}"
    elif mode == 'multi_target':
        command = f"{base_command}-targets {target}"
    elif mode == 'network_scan':
        command = f"{base_command}-target {target}"
    elif mode == 'custom_template':
        command = f"{base_command}-u {additional_param[0]} -t {additional_param[1]}"
    elif mode == 'dashboard':
        command = f"{base_command}-target {target} -dashboard"

    if command:
        await run_command(command, output_name="nuclei")

def get_severity():
    return input(f"{Fore.GREEN}Digite a severidade (low, medium, high) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def get_multi_target_file():
    return input(f"{Fore.GREEN}Digite o caminho para o arquivo com a lista de alvos ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")

def get_network_target():
    while True:
        target = input(f"{Fore.GREEN}Digite o alvo da rede (EX: 192.168.1.0/24) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")
        if target.lower() == 'b':
            return None
        if is_valid_cidr(target):
            return target
        else:
            logger.error(f"Formato inválido. Por favor, insira um endereço CIDR válido.")

def get_custom_template():
    target = input(f"{Fore.GREEN}Digite o endereço do alvo (EX: 192.168.0.1 | site.com) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")
    if target.lower() == 'b':
        return (None, None)

    template = input(f"{Fore.GREEN}Digite o caminho para o template personalizado (EX: /path/to/template.yaml) ou {Fore.RED}[B]{Fore.GREEN} para voltar: ")
    if template.lower() == 'b':
        return (None, None)

    return (target, template)

async def nuclei_options(option):
    target = global_target.value or await session.prompt_async(f"{Fore.RED}Digite o alvo ou [B] para voltar: ")

    if option in ["1", "2", "6"] and target:

        if option == "1":
            if target.lower() == 'b':
                clear_terminal()
                return
            await nuclei(target, 'target_spec')
        elif option == "2":
            if target.lower() == 'b':
                clear_terminal()
                return
            severity = get_severity()
            if severity.lower() == 'b':
                clear_terminal()
                return
            await nuclei(target, 'severity', severity)
        elif option == "6":
            if target.lower() == 'b':
                clear_terminal()
                return
            await nuclei(target, 'dashboard')
    elif option == "3":
        if target.lower() == 'b':
                clear_terminal()
                return
        target = get_multi_target_file()
        await nuclei(target, 'multi_target')

    elif option == "5":
        target, template = get_custom_template()
        if target is None or template is None:
            clear_terminal()
            return
        await nuclei(target, 'custom_template', (target, template))

async def nuclei_menu_loop():
    while True:
        clear_terminal()
        global_target_display = (
            f"Alvo: {Fore.GREEN}{global_target.value}{Fore.RESET}"
            if global_target.value
            else f"Alvo: {Fore.RED}Não definido{Fore.RESET}"
        )
        
        print(rf"""{Fore.BLUE}
         _   _            _      _ Pressione Ctrl+T para definir o alvo
        | \ | |          | |    (_)     {Fore.YELLOW}{global_target_display}{Fore.BLUE}
        |  \| |_   _  ___| | ___ _ 
        | . ` | | | |/ __| |/ _ \ |
        | |\  | |_| | (__| |  __/ |
        |_| \_|\__,_|\___|_|\___|_|
                                    
        {Fore.CYAN}[1] {Fore.RESET}Varredura padrão {get_command_explanation('target_spec') if is_info_visible() else ""}
        {Fore.CYAN}[2] {Fore.RESET}Filtrar por severidade {get_command_explanation('severity') if is_info_visible() else ""}
        {Fore.CYAN}[3] {Fore.RESET}Varredura múltipla {get_command_explanation('multi_target') if is_info_visible() else ""}
        {Fore.CYAN}[4] {Fore.RESET}Varredura de rede {get_command_explanation('network_scan') if is_info_visible() else ""}
        {Fore.CYAN}[5] {Fore.RESET}Usar template personalizado {get_command_explanation('custom_template') if is_info_visible() else ""}
        {Fore.CYAN}[6] {Fore.RESET}Enviar para ProjectDiscovery {get_command_explanation('dashboard') if is_info_visible() else ""}
        {Fore.RED}[B] {Fore.RESET}Voltar
        {Fore.YELLOW}[I] {Fore.RESET}Alternar Informações
        """)

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)
    
        if option.lower() == 'b':
            break
        elif option.lower() == 'i':
            toggle_info()
            continue
        elif option == "4":
            target = get_network_target()
            if target is None:
                clear_terminal()
                break
            await nuclei(target, 'network_scan')
        if option in [str(i) for i in range(1, 7)]:
            await nuclei_options(option)


