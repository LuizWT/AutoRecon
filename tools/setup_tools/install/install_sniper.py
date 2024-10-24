import os
from colorama import init, Fore

init(autoreset=True)

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
