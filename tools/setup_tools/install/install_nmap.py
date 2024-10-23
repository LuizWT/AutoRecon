import os
import platform
from colorama import init, Fore

init(autoreset=True)

def install_nmap():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do Nmap...")
        
        if platform.system() == 'Linux':
            if os.path.isfile('/etc/debian_version'):
                os.system('sudo apt-get update && sudo apt-get install -y nmap')
            elif os.path.isfile('/etc/redhat-release'):
                os.system('sudo dnf install -y nmap')
            elif os.path.isfile('/etc/arch-release'):
                os.system('sudo pacman -Syu --noconfirm nmap')
            elif os.path.isfile('/etc/SuSE-release'):
                os.system('sudo zypper refresh && sudo zypper install -y nmap')
            else:
                print(f"{Fore.RED}[ERROR] Distribuição não suportada para instalação do Nmap.")
                return
            print(f"{Fore.CYAN}[INFO] Nmap instalado com sucesso.")
        else:
            print(f"{Fore.RED}[ERROR] Este script só suporta instalação no Linux.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação: {e}")