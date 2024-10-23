import subprocess
from colorama import init, Fore

init(autoreset=True)

def check_wpscan():
    try:
        subprocess.run(['wpscan', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] WPScan já está instalado.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}[INFO] WPScan não está instalado.")
        return False