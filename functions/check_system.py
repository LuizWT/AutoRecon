import os
import sys
import platform
from colorama import init, Fore

init(autoreset=True)  # inicia o colorama

def check_system():
    if platform.system() != "Linux":
        print(f"{Fore.RED}[ERRO] Este programa só pode ser executado em sistemas Linux.")
        return False
    if os.geteuid() != 0:
        print(f"{Fore.RED}[ERRO] É necessário executar como ROOT.")
        return False
    return True