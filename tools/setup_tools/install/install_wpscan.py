import os
import subprocess
from colorama import init, Fore
from tools.setup_tools.check.check_ruby import check_ruby
from tools.setup_tools.install.install_ruby  import install_ruby

init(autoreset=True)

def install_wpscan():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do WPScan...")
        if not check_ruby():
            install_ruby_choice = input(f"{Fore.YELLOW}[INFO] Ruby não está instalado. Deseja instalar Ruby? (y/n): ").lower()
            if install_ruby_choice in ['s', 'y']:
                install_ruby()
            else:
                print(f"{Fore.RED}[INFO] WPScan não pode ser instalado sem Ruby.")
                return

        os.system('sudo gem install wpscan')  # Usar gem para instalar o WPScan
        print(f"{Fore.CYAN}[INFO] WPScan instalado com sucesso.")
        
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação do WPScan: {e}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro inesperado: {e}")