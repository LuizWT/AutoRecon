import os
import platform

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

