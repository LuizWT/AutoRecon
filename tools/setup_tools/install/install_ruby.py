import os
import platform
from colorama import init, Fore

init(autoreset=True)

def install_ruby():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do Ruby...")
        if platform.system() == 'Linux':
            if os.path.isfile('/etc/debian_version'):
                os.system('sudo apt-get update && sudo apt-get install -y ruby')
            elif os.path.isfile('/etc/redhat-release'):
                os.system('sudo dnf install -y ruby')
            elif os.path.isfile('/etc/arch-release'):
                os.system('sudo pacman -Syu --noconfirm ruby')
            elif os.path.isfile('/etc/SuSE-release'):
                os.system('sudo zypper refresh && sudo zypper install -y ruby')
            else:
                print(f"{Fore.RED}[ERROR] Distribuição não suportada para instalação do Ruby.")
                return
            print(f"{Fore.CYAN}[INFO] Ruby instalado com sucesso.")
        else:
            print(f"{Fore.RED}[ERROR] Este script só suporta instalação no Linux.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação: {e}")

