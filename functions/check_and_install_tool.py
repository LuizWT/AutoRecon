from colorama import Fore, init
from functions.clear_terminal import clear_terminal

init(autoreset=True)

def check_and_install_tool(tool_name, check_func, install_func, menu_func, dep_check_func=None, dep_install_func=None):
    print(f"{Fore.GREEN}[INFO] Verificando a instalação do {tool_name}...")
    if check_func():
        print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")
        clear_terminal()
        menu_func()
    else:
        if dep_check_func and not check_func():  # Faz a verificação de dependência apenas se a ferramenta não estiver instalada
            install_dep = input(f"{Fore.YELLOW}[INFO] {tool_name} requer uma dependência. Deseja instalar? (y/n): ").lower()
            if install_dep in ['s', 'y']:
                dep_install_func()

        install_choice = input(f"{Fore.YELLOW}[INFO] {tool_name} não está instalado. Deseja instalar o {tool_name}? (y/n): ").lower()
        if install_choice in ['s', 'y']:
            install_func()
            print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")
            clear_terminal()
            menu_func()
        else:
            print(f"{Fore.RED}[INFO] Retornando ao menu principal...")

