# Importações padrão de Python
import readline
import asyncio
import sys
import os
# Bibliotecas de terceiros
from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML  # Formatar o texto com HTML no prompt_toolkit pois não é possível usar o colorama
from prompt_toolkit.key_binding import KeyBindings

# Importações internas de funções específicas
from functions.check_system import check_system  # Verifica se o sistema é Linux
from functions.clear_terminal import clear_terminal  # Limpar o terminal
from functions.check_and_install_tool import check_and_install_tool  # Função genérica para checar e instalar ferramentas
from functions.set_global_target import set_global_target, bindings, global_target  # Funções e variáveis para configuração do alvo global
from configurations.ar_updater import parse_args, update_repository, new_version_checker # Verifica se a ferramenta está atualizada
from configurations.configure_alias import configure_global_command  # Configura o alias global "autorecon"
from configurations.version import __version__
# Importação de configurações e ferramentas
from setup_tools.setup import TOOLS_CONFIG, install_tool
from tools.submenu.automation_submenu import automation_setup_menu
from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from tools.wpscan import wpscan_menu_loop
from tools.nuclei import nuclei_menu_loop
from tools.nikto import nikto_menu_loop
from functions.proxy_chains import ProxyManager 

# Inicializa a colorama e cria a sessão para receber entradas de forma interativa
init(autoreset=True)
session = PromptSession()

# Função que exibe o menu principal
def main_menu():
    if new_version_checker():
        update_message = f"{Fore.RED}Outdated{Fore.YELLOW} - @LuizWt {Fore.RED}\nUtilize 'sudo autorecon --update' para atualizar"
    else:
        update_message = f"{Fore.GREEN}Latest{Fore.YELLOW} - @LuizWt"
    configure_global_command()
    proxychains_info = " (/etc/proxychains.conf)" if ProxyManager.check_installed() else ""
    proxychains_status = f"{Fore.GREEN}ON" if ProxyManager.is_enabled() else f"{Fore.RED}OFF"
    
    global_target_display = (
        f"Alvo: {Fore.GREEN}{global_target.value}{Fore.RESET}"
        if global_target.value
        else f"Alvo: {Fore.RED}Não definido{Fore.RESET}"
    )
    automation_commands = f"{Fore.GREEN}ON" if global_target.value else f"{Fore.RED}OFF"
    print(rf"""
    {Fore.BLUE}{Style.BRIGHT}
                _        _____                      
     /\        | |      |  __ \      Pressione Ctrl+T para definir o alvo               
    /  \  _   _| |_ ___ | |__) |___  ___ ___  _ __ {Fore.YELLOW}{global_target_display}{Fore.BLUE}{Style.BRIGHT}
   / /\ \| | | | __/ _ \|  _  // _ \/ __/ _ \| '_ \ 
  / ____ \ |_| | || (_) | | \ \  __/ (_| (_) | | | |
 /_/    \_\__,_|\__\___/|_|  \_\___|\___\___/|_| |_|

 {Fore.YELLOW}+ -- --=[ https://github.com/LuizWT/
 {Fore.YELLOW}+ -- --=[ AutoRecon {__version__} {update_message}

    {Fore.CYAN}[1] {Fore.RESET}SNIPER
    {Fore.CYAN}[2] {Fore.RESET}NMAP
    {Fore.CYAN}[3] {Fore.RESET}WPSCAN
    {Fore.CYAN}[4] {Fore.RESET}NUCLEI
    {Fore.CYAN}[5] {Fore.RESET}NIKTO
    {Fore.CYAN}[0] {Fore.RESET}ProxyChains [{proxychains_status}{Fore.RESET}] {proxychains_info}
    {Fore.RED}[9] {Fore.RESET}Sair
    {Fore.YELLOW}[CTRL+A] {Fore.RESET}Automação de comandos [{automation_commands}{Fore.RESET}]
    """)

# Função assíncrona Main
async def main_loop():

    # Função de atalho para automação de comandos (Ctrl+A)
    bindings = KeyBindings()
    @bindings.add('c-a')
    async def _(event):
        if global_target.value:
            clear_terminal()
            await automation_setup_menu()
        else:
            clear_terminal()
            print(f"{Fore.RED}Você deve definir um alvo global antes de acessar este submenu.\n{Fore.CYAN}Pressione Enter para retornar...")
            return
    
    @bindings.add('c-t')
    def _(event):
        asyncio.create_task(set_global_target())


    OPTIONS = {
        "1": ("sniper", sniper_menu_loop),
        "2": ("nmap", nmap_menu_loop),
        "3": ("wpscan", wpscan_menu_loop),
        "4": ("nuclei", nuclei_menu_loop),
        "5": ("nikto", nikto_menu_loop)
    }

    if not check_system():
        return

    while True:
        clear_terminal()
        main_menu()

        option = await session.prompt_async(HTML(f"<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings)

        if option == "9":
            clear_terminal()
            print(f"{Fore.RED}[INFO] Saindo do AutoRecon.")
            break

        elif option in OPTIONS:
            tool_name, menu_func = OPTIONS[option]
            clear_terminal()
            await check_and_install_tool(tool_name, menu_func, global_target.value)

        elif option == "0":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do ProxyChains...")

            if ProxyManager.check_installed():
                ProxyManager.toggle()
            else:
                install_choice = await session.prompt_async(HTML(f"<ansiyellow>[INFO] ProxyChains não está instalado. Deseja instalar o ProxyChains? (y/n): </ansiyellow>"))
                if install_choice.lower() in ['s', 'y']:
                    install_tool("proxychains")
                    # Aqui é o importante: depois da instalação, verificar de novo
                    if ProxyManager.check_installed():
                        ProxyManager.toggle()
                    else:
                        print(f"{Fore.RED}[ERROR] Falha ao instalar o ProxyChains.")
                    input(f"{Fore.YELLOW}Pressione Enter para retornar ao menu principal...")
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
                    input(f"{Fore.YELLOW}Pressione Enter para retornar ao menu principal...")


if __name__ == "__main__":
    args = parse_args()
    if args.update:
        update_repository()
        sys.exit(0)

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        clear_terminal()
        print(f"{Fore.RED}[INFO] Saindo do AutoRecon via Ctrl+C.")
