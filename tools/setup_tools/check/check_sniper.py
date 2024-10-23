import subprocess
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