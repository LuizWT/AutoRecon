import os
import platform
from tools.setup_tools import setup_tools
from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from colorama import init, Fore, Style


init(autoreset=True)  # inicia o colorama

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def main_menu():
    print(f"""
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
    setup_tools()
    while True:
        clear_screen()
        main_menu()
        option = input(f"{Fore.YELLOW}Escolha uma opção: ")
        if option == "9":
            clear_screen()
            print(f"{Fore.RED}[INFO] Saindo do AutoRecon.")
            break
        elif option == "1":
            clear_screen()
            print(f"{Fore.GREEN}[INFO] Abrindo o menu SNIPER...")
            sniper_menu_loop()
        elif option == "2":
            clear_screen()
            print(f"{Fore.GREEN}[INFO] Abrindo o menu NMAP...")
            nmap_menu_loop()

if __name__ == "__main__":
    main()
