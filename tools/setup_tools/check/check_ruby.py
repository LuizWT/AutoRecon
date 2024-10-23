import subprocess
from colorama import init, Fore

init(autoreset=True)

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