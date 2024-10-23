import subprocess
from colorama import init, Fore

init(autoreset=True)

def check_nmap():
    try:
        subprocess.run(['nmap', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] Nmap já está instalado.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}[INFO] Nmap não está instalado.")
        return False
