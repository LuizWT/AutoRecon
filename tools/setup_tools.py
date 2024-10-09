import os
import subprocess
import platform
from colorama import init, Fore

init(autoreset=True)

def check_sniper():
    try:
        subprocess.run(['sudo', 'sniper', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] Sn1per já está instalado.")
        return True
    except subprocess.CalledProcessError:
        print(f"{Fore.CYAN}[INFO] Sn1per não está instalado.")
        return False

def install_sniper():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do Sn1per...")
        if platform.system() == 'Linux':
            if not os.path.exists('Sn1per'):
                os.system('git clone https://github.com/1N3/Sn1per')
            os.chdir('Sn1per')
            os.system('sudo bash install.sh')
            print(f"{Fore.CYAN}[INFO] Sn1per instalado com sucesso.")
        else:
            print(f"{Fore.RED}[ERROR] Este script só suporta instalação no Linux.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação: {e}")

def check_nmap():
    try:
        subprocess.run(['nmap', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] Nmap já está instalado.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}[INFO] Nmap não está instalado. Iniciando a instalação...")
        install_nmap()
        return False

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

def setup_tools():
    if not check_sniper():
        install_sniper()
    check_nmap()

setup_tools()

