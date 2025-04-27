import os
import sys
import platform
from colorama import init, Fore

init(autoreset=True)  # inicia o colorama

def check_system():
    if platform.system() != "Linux":
        print(f"{Fore.RED}[ERRO] Este programa só pode ser executado em sistemas Linux.")
        sys.exit(1)
    if os.geteuid() != 0:
        print(f"{Fore.RED}[ERRO] É necessário executar como ROOT.")
        sys.exit(1)
    return True
