# Importações padrão de Python
import readline
import asyncio
import argparse
import sys

# Bibliotecas de terceiros
from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML  # Formatar o texto com HTML no prompt_toolkit pois não é possível usar o colorama

# Importações internas de funções específicas
from functions.check_system import check_system  # Função personalizada de verificação do sistema
from functions.clear_terminal import clear_terminal  # Função personalizada para limpar o terminal
from functions.check_and_install_tool import check_and_install_tool  # Função personalizada para checar e instalar ferramentas
from functions.set_global_target import set_global_target, bindings, state  # Funções e variáveis para configuração do alvo global
from functions.ar_updater import is_git_repo, update_repository # verifica se a ferramenta está atualizada

# Importação de configurações e ferramentas
from setup_tools.setup import TOOLS_CONFIG, install_tool, check_proxychains
from tools.submenu.automation_submenu import automation_setup_menu
from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from tools.wpscan import wpscan_menu_loop
from tools.nuclei import nuclei_menu_loop
from tools.nikto import nikto_menu_loop
from functions.proxy_chains import toggle_proxychains, proxychains_enabled, check_proxychains_installed

# Inicializa a colorama e cria a sessão para receber entradas de forma interativa
init(autoreset=True)
session = PromptSession()


# Função de atalho para automação de comandos (Ctrl+A)
@bindings.add('c-a')
async def _(event):
    if state['global_target']:
        clear_terminal()
        await automation_setup_menu()
    else:
        clear_terminal()
        print(f"{Fore.RED}Você deve definir um alvo global antes de acessar este submenu.\n{Fore.CYAN}Pressione Enter para retornar...")
        return


# Função que exibe o menu principal
def main_menu():
    proxychains_info = " (/etc/proxychains.conf)" if check_proxychains_installed() else ""
    proxychains_status = f"{Fore.GREEN}ON" if proxychains_enabled else f"{Fore.RED}OFF"
    
    global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"
    automation_commands = f"{Fore.GREEN}ON" if state['global_target'] else f"{Fore.RED}OFF"
    print(rf"""
    {Fore.BLUE}{Style.BRIGHT}
                _        _____                      
     /\        | |      |  __ \      Pressione Ctrl+T para definir o alvo               
    /  \  _   _| |_ ___ | |__) |___  ___ ___  _ __ {Fore.YELLOW}{global_target_display}{Fore.BLUE}{Style.BRIGHT}
   / /\ \| | | | __/ _ \|  _  // _ \/ __/ _ \| '_ \ 
  / ____ \ |_| | || (_) | | \ \  __/ (_| (_) | | | |
 /_/    \_\__,_|\__\___/|_|  \_\___|\___\___/|_| |_|

 {Fore.YELLOW}+ -- --=[ https://github.com/LuizWT/
 {Fore.YELLOW}+ -- --=[ AutoRecon v1.2 - @LuizWt

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
    global proxychains_enabled

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
        elif option == "1":
            clear_terminal()
            await check_and_install_tool("sniper", sniper_menu_loop, state['global_target'])
        elif option == "2":
            clear_terminal()
            await check_and_install_tool("nmap", nmap_menu_loop, state['global_target'])
        elif option == "3":
            clear_terminal()
            await check_and_install_tool("wpscan", wpscan_menu_loop, state['global_target'])
        elif option == "4":
            clear_terminal()
            await check_and_install_tool("nuclei", nuclei_menu_loop, state['global_target'])
        elif option == "5":
            clear_terminal()
            await check_and_install_tool("nikto", nikto_menu_loop, state['global_target'])
        elif option == "0":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do ProxyChains...")

            if check_proxychains():
                proxychains_enabled = toggle_proxychains()
                status = 'ON' if proxychains_enabled else 'OFF'
                color = Fore.GREEN if proxychains_enabled else Fore.RED
                print(f"{Fore.GREEN}[INFO] ProxyChains [{color}{status}{Fore.RESET}].")
            else:
                install_choice = await session.prompt_async(HTML(f"<ansiyellow>[INFO] ProxyChains não está instalado. Deseja instalar o ProxyChains? (y/n): </ansiyellow>"))
                if install_choice.lower() in ['s', 'y']:
                    install_tool("proxychains")
                    if check_proxychains():
                        proxychains_enabled = toggle_proxychains()
                        print(f"{Fore.GREEN}[INFO] ProxyChains ativado [{Fore.GREEN}ON{Fore.RESET}].")
                    else:
                        print(f"{Fore.RED}[ERROR] Falha ao instalar o ProxyChains.")
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")

def parse_args():
    parser = argparse.ArgumentParser(description="AutoRecon - Ferramenta de Automação de Segurança")
    parser.add_argument('-update', action='store_true', help="Atualiza o código para a versão mais recente")
    return parser.parse_args()

if __name__ == "__main__":
    # Verificar se foi chamado para atualizar o código
    args = parse_args()
    if args.update:
        update_repository()  # Atualiza o código
        sys.exit(0)  # Finaliza o programa após a atualização

    asyncio.run(main_loop())