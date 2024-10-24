import os
from colorama import init, Fore
import subprocess
init(autoreset=True)

def check_nmap():
    try:
        subprocess.run(['nmap', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] Nmap já está instalado.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}[INFO] Nmap não está instalado.")
        return False

def check_wpscan():
    try:
        subprocess.run(['wpscan', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] WPScan já está instalado.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}[INFO] WPScan não está instalado.")
        return False
    
def check_sniper():
    try:
        subprocess.run(['sudo', 'sniper', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] Sn1per já está instalado.")
        return True
    except subprocess.CalledProcessError:
        print(f"{Fore.CYAN}[INFO] Sn1per não está instalado.")
        return False

def check_ruby():
    try:
        result = subprocess.run(['ruby', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        version_output = result.stdout.decode().split()[1]
        version_parts = version_output.split('.')

        # Verifica se a versão é >= 3.0.0
        major_version = int(version_parts[0])
        minor_version = int(version_parts[1])

        if major_version > 3 or (major_version == 3 and minor_version >= 0):
            print(f"{Fore.CYAN}[INFO] Ruby versão {version_output} já está instalado e é compatível.")
            return True
        else:
            print(f"{Fore.RED}[INFO] Ruby versão {version_output} é incompatível. Versão 3.0 ou superior é necessária.")
            return False
    except (FileNotFoundError, IndexError, ValueError):
        print(f"{Fore.RED}[INFO] Ruby não está instalado ou houve um erro ao verificar a versão.")
        return False
    
def check_proxychains():
    try:
        subprocess.run(['proxychains4', 'true'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] ProxyChains já está instalado.")
        return True
    except FileNotFoundError:
        print(f"{Fore.RED}[INFO] ProxyChains não está instalado.")
        return False
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}[INFO] ProxyChains não está funcionando corretamente.")
        return False
    

def install_nmap():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do Nmap...")
        
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
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação do Nmap: {e}")

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

        os.system('sudo gem install wpscan')
        print(f"{Fore.CYAN}[INFO] WPScan instalado com sucesso.")
        
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação do WPScan: {e}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro inesperado: {e}")

def install_sniper():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do Sn1per...")

        if not os.path.exists('Sn1per'):
            os.system('git clone https://github.com/1N3/Sn1per')
        
        os.chdir('Sn1per')
        os.system('sudo bash install.sh')

        print(f"{Fore.CYAN}[INFO] Sn1per instalado com sucesso.")
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação do Sn1per: {e}")

def install_ruby():
    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do Ruby...")

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
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação do Ruby: {e}")

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
