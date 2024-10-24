import os
from colorama import init, Fore

init(autoreset=True)

def install_proxychains():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do ProxyChains...")
        
        if os.path.isfile('/etc/debian_version'):
            os.system('sudo apt-get update && sudo apt-get install -y proxychains-ng')
        elif os.path.isfile('/etc/redhat-release'):
            os.system('sudo dnf install -y proxychains-ng')
        elif os.path.isfile('/etc/arch-release'):
            os.system('sudo pacman -Syu --noconfirm proxychains-ng')
        elif os.path.isfile('/etc/SuSE-release'):
            os.system('sudo zypper refresh && sudo zypper install -y proxychains-ng')
        else:
            print(f"{Fore.RED}[ERROR] Distribuição não suportada para instalação do ProxyChains.")
            return

        print(f"{Fore.CYAN}[INFO] ProxyChains instalado com sucesso.")
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação do ProxyChains: {e}")
