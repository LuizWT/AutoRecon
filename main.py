import readline
from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
import asyncio

from functions.check_system import check_system
from functions.clear_terminal import clear_terminal
from functions.check_and_install_tool import check_and_install_tool
from functions.set_global_target import set_global_target, bindings, state 

from setup_tools.setup import TOOLS_CONFIG, install_tool, check_proxychains

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
                install_choice = input(f"{Fore.YELLOW}[INFO] ProxyChains não está instalado. Deseja instalar o ProxyChains? (y/n): ").lower()
                if install_choice in ['s', 'y']:
                    install_tool("proxychains")
                    if check_proxychains():
                        proxychains_enabled = toggle_proxychains()
                        print(f"{Fore.GREEN}[INFO] ProxyChains ativado [{Fore.GREEN}ON{Fore.RESET}].")
                    else:
                        print(f"{Fore.RED}[ERROR] Falha ao instalar o ProxyChains.")
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")

if __name__ == "__main__":
    asyncio.run(main_loop())
