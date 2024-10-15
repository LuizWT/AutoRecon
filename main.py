import os
from functions.clear_terminal import clear_terminal
from tools.setup_tools import check_sniper, install_sniper, check_nmap, install_nmap
from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from colorama import init, Fore, Style

init(autoreset=True)  # inicia o colorama

def main_menu():
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
    {Fore.RED}[9] {Fore.RESET}Sair
    """)

def main():
    # Verifica se o usuário já é root
    if os.geteuid() != 0:
        print(f"{Fore.RED}[ERRO] Esta ferramenta precisa de privilégios ROOT para funcionar.")
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
                install = input(f"{Fore.YELLOW}[INFO] Sn1per não está instalado. Deseja instalar o Sn1per? (s/n): ").lower()
                if install == 's' or install == 'y':
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
                install = input(f"{Fore.YELLOW}[INFO] Nmap não está instalado. Deseja instalar o Nmap? (s/n): ").lower()
                if install == 's' or install == 'y':
                    install_nmap()
                    print(f"{Fore.GREEN}[INFO] Abrindo o menu NMAP...")
                    clear_terminal()
                    nmap_menu_loop()
                else:
                    print(f"{Fore.RED}[INFO] Retornando ao menu principal...")

if __name__ == "__main__":
    main()
