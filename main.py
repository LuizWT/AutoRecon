import readline
from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
import asyncio

from functions.check_system import check_system
from functions.clear_terminal import clear_terminal
from functions.check_and_install_tool import check_and_install_tool
from functions.set_global_target import set_global_target, bindings, state 

from setup_tools.setup import (
    check_nmap, check_wpscan, check_sniper, check_ruby, check_proxychains, check_go, check_nuclei, check_nikto,
    install_nmap, install_wpscan, install_sniper, install_ruby, install_proxychains, install_go, install_nuclei, install_nikto,
)

from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from tools.wpscan import wpscan_menu_loop
from tools.nuclei import nuclei_menu_loop
from tools.nikto import nikto_menu_loop
from functions.proxy_chains import toggle_proxychains, proxychains_enabled, check_proxychains_installed

init(autoreset=True)

session = PromptSession()

def main_menu():
    proxychains_info = " (/etc/proxychains.conf)" if check_proxychains_installed() else ""
    proxychains_status = f"{Fore.GREEN}ON" if proxychains_enabled else f"{Fore.RED}OFF"
    
    global_target_display = f"Alvo: {state['global_target']}" if state['global_target'] else "Alvo: Não definido"
    
    print(rf"""
    {Fore.BLUE}{Style.BRIGHT}
                _        _____                      
     /\        | |      |  __ \      Pressione Ctrl+T para definir o alvo               
    /  \  _   _| |_ ___ | |__) |___  ___ ___  _ __ {Fore.YELLOW}{global_target_display}{Fore.BLUE}{Style.BRIGHT}
   / /\ \| | | | __/ _ \|  _  // _ \/ __/ _ \| '_ \ 
  / ____ \ |_| | || (_) | | \ \  __/ (_| (_) | | | |
 /_/    \_\__,_|\__\___/|_|  \_\___|\___\___/|_| |_|
                                            LuizWt{Style.RESET_ALL}

    {Fore.CYAN}[1] {Fore.RESET}SNIPER
    {Fore.CYAN}[2] {Fore.RESET}NMAP
    {Fore.CYAN}[3] {Fore.RESET}WPSCAN
    {Fore.CYAN}[4] {Fore.RESET}NUCLEI
    {Fore.CYAN}[5] {Fore.RESET}NIKTO
    {Fore.CYAN}[0] {Fore.RESET}ProxyChains [{proxychains_status}{Fore.RESET}] {proxychains_info}
    {Fore.RED}[9] {Fore.RESET}Sair
    """)


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
            check_and_install_tool("Sn1per", check_sniper, install_sniper, sniper_menu_loop, state['global_target'])
        elif option == "2":
            clear_terminal()
            check_and_install_tool("Nmap", check_nmap, install_nmap, nmap_menu_loop, state['global_target'])
        elif option == "3":
            clear_terminal()
            check_and_install_tool("WPScan", check_wpscan, install_wpscan, wpscan_menu_loop, state['global_target'], dep_check_func=check_ruby, dep_install_func=install_ruby)
        elif option == "4":
            clear_terminal()
            check_and_install_tool("Nuclei", check_nuclei, install_nuclei, nuclei_menu_loop, state, dep_check_func=check_go, dep_install_func=install_go)
        elif option == "5":
            clear_terminal()
            check_and_install_tool("Nikto", check_nikto, install_nikto, nikto_menu_loop, state['global_target'])

        elif option == "0":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do ProxyChains...")
            if check_proxychains():
                proxychains_enabled = toggle_proxychains()
                print(f"{Fore.GREEN}[INFO] ProxyChains [{Fore.GREEN if proxychains_enabled else Fore.RED}{'ON' if proxychains_enabled else 'OFF'}{Fore.RESET}].")
            else:
                install = input(f"{Fore.YELLOW}[INFO] ProxyChains não está instalado. Deseja instalar o ProxyChains? (y/n): ").lower()
                if install in ['s', 'y']:
                    install_proxychains()
                    if check_proxychains():
                        proxychains_enabled = toggle_proxychains()
                        print(f"{Fore.GREEN}[INFO] ProxyChains ativado [{Fore.GREEN}ON{Fore.RESET}].")
                    else:
                        print(f"{Fore.RED}[ERROR] Falha ao instalar o ProxyChains.")
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")

if __name__ == "__main__":
    asyncio.run(main_loop())
