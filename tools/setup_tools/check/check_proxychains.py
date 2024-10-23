import subprocess
from colorama import init, Fore

init(autoreset=True)

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