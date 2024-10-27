from functions.check_system import check_system
from functions.clear_terminal import clear_terminal
from setup_tools.setup import check_nmap, check_wpscan, check_sniper, check_ruby, check_proxychains, check_go, check_nuclei, check_nikto
from setup_tools.setup import install_nmap, install_wpscan, install_sniper, install_ruby, install_proxychains, install_go, install_nuclei, install_nikto
from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from tools.wpscan import wpscan_menu_loop
from tools.nuclei import nuclei_menu_loop
from tools.nikto import nikto_menu_loop
from functions.proxy_chains import toggle_proxychains, proxychains_enabled, check_proxychains_installed
from colorama import init, Fore, Style
import readline

init(autoreset=True)  # inicia o colorama

def main_menu():
    proxychains_info = " (/etc/proxychains.conf)" if check_proxychains_installed() else ""
    status_color = Fore.GREEN if proxychains_enabled else Fore.RED
    status_text = "ON" if proxychains_enabled else "OFF"
    print(rf"""
    {Fore.BLUE}{Style.BRIGHT}
                _        _____                      
     /\        | |      |  __ \                     
    /  \  _   _| |_ ___ | |__) |___  ___ ___  _ __  
   / /\ \| | | | __/ _ \|  _  // _ \/ __/ _ \| '_ \ 
  / ____ \ |_| | || (_) | | \ \  __/ (_| (_) | | | |
 /_/    \_\__,_|\__\___/|_|  \_\___|\___\___/|_| |_|
                                            LuizWt{Style.RESET_ALL}

    {Fore.CYAN}[1] {Fore.RESET}SNIPER
    {Fore.CYAN}[2] {Fore.RESET}NMAP
    {Fore.CYAN}[3] {Fore.RESET}WPSCAN
    {Fore.CYAN}[4] {Fore.RESET}NUCLEI
    {Fore.CYAN}[5] {Fore.RESET}NIKTO
    {Fore.CYAN}[0] {Fore.RESET}ProxyChains [{status_color}{status_text}{Fore.RESET}] {proxychains_info}
    {Fore.RED}[9] {Fore.RESET}Sair
    """)

def main():
    global proxychains_enabled

    if not check_system():
        return

    while True:
        clear_terminal()
        main_menu()
        option = input(f"{Fore.YELLOW}Escolha uma opção: ")

        if option == "9":
            clear_terminal()
            print(f"{Fore.RED}[INFO] Saindo do AutoRecon.")
            break
        elif option == "1":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do Sn1per...")
            if check_sniper():
                print(f"{Fore.GREEN}[INFO] Abrindo o menu SNIPER...")
                clear_terminal()
                sniper_menu_loop()
            else:
                install = input(f"{Fore.YELLOW}[INFO] Sn1per não está instalado. Deseja instalar o Sn1per? (y/n): ").lower()
                if install in ['s', 'y']:
                    install_sniper()
                    print(f"{Fore.GREEN}[INFO] Abrindo o menu SNIPER...")
                    clear_terminal()
                    sniper_menu_loop()
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
        elif option == "2":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do Nmap...")
            if check_nmap():
                print(f"{Fore.GREEN}[INFO] Abrindo o menu NMAP...")
                clear_terminal()
                nmap_menu_loop()
            else:
                install = input(f"{Fore.YELLOW}[INFO] Nmap não está instalado. Deseja instalar o Nmap? (y/n): ").lower()
                if install in ['s', 'y']:
                    install_nmap()
                    print(f"{Fore.GREEN}[INFO] Abrindo o menu NMAP...")
                    clear_terminal()
                    nmap_menu_loop()
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
        elif option == "3":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do WPScan...")
            if check_wpscan(): # WPScan DEVE ser verificado primeiro
                print(f"{Fore.GREEN}[INFO] Abrindo o WPScan...")
                clear_terminal()
                wpscan_menu_loop()
            else:
                if check_ruby():
                    install_wpscan_choice = input(f"{Fore.YELLOW}[INFO] Deseja instalar o WPScan? (y/n): ").lower()
                    if install_wpscan_choice in ['s', 'y']:
                        install_wpscan()
                    else:
                        print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
                else:
                    install_ruby_choice = input(f"{Fore.YELLOW}[INFO] Ruby não está instalado. Deseja instalar Ruby e WPScan? (y/n): ").lower()
                    if install_ruby_choice in ['s', 'y']:
                        install_ruby()
                        install_wpscan()
                    else:
                        print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
        elif option == "4":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do Nuclei...")
            if check_nuclei(): # Nuclei DEVE ser verificado primeiro
                print(f"{Fore.GREEN}[INFO] Abrindo o Nuclei...")
                clear_terminal()
                nuclei_menu_loop()
            else:
                if check_go():
                    install_nuclei_choice = input(f"{Fore.YELLOW}[INFO] Deseja instalar o Nuclei? (y/n): ").lower()
                    if install_nuclei_choice in ['s', 'y']:
                        install_nuclei()
                    else:
                        print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
                else:
                    install_go_choice = input(f"{Fore.YELLOW}[INFO] GO não está instalado. Deseja instalar GO e Nuclei? (y/n): ").lower()
                    if install_go_choice in ['s', 'y']:
                        install_go()
                        install_nuclei()
        elif option == "5":
            clear_terminal()
            print(f"{Fore.GREEN}[INFO] Verificando a instalação do Nikto...")
            if check_nikto():
                print(f"{Fore.GREEN}[INFO] Abrindo o menu NIKTO...")
                clear_terminal()
                nikto_menu_loop()
            else:
                install = input(f"{Fore.YELLOW}[INFO] Nikto não está instalado. Deseja instalar o Nikto? (y/n): ").lower()
                if install in ['s', 'y']:
                    install_nikto()
                    print(f"{Fore.GREEN}[INFO] Abrindo o menu NIKTO...")
                    clear_terminal()
                    nikto_menu_loop()
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
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
    main()
