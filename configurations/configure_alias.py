import os
import stat
import subprocess
from colorama import Fore, init

init(autoreset=True)

CONFIG_FILE = "/etc/autorecon_path.conf"

def configure_global_command():
    script_name = "autorecon"
    target_path = f"/usr/local/bin/{script_name}"

    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../autorecon.py"))

    if os.path.exists(target_path):
        return

    launcher_content = f"""#!/bin/bash
if [ -f {CONFIG_FILE} ]; then
    script_path=$(cat {CONFIG_FILE})
    if [ -f "$script_path" ]; then
        sudo python3 "$script_path" "$@"
    else
        echo "[ERROR]: O arquivo $script_path não foi encontrado. Reconfigure o 'autorecon'\n\nAtualize o diretório da ferramenta em 'sudo nano /etc/autorecon_path.conf'"
    fi
else
    echo "[ERROR]: Arquivo de configuração {CONFIG_FILE} não encontrado. Reconfigure o 'autorecon'\n\n'Atualize o diretório da ferramenta em 'sudo nano /etc/autorecon_path.conf'"
fi
"""

    try:
        with open(script_name, "w") as f:
            f.write(launcher_content)
        os.chmod(script_name, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        subprocess.run(["sudo", "mv", script_name, target_path], check=True)

        with open("autorecon_path.conf", "w") as conf:
            conf.write(script_path)
        subprocess.run(["sudo", "mv", "autorecon_path.conf", CONFIG_FILE], check=True)

        print(f"{Fore.GREEN}Comando '{script_name}' configurado com sucesso em {target_path}.\n")
        print(f"{Fore.GREEN}O arquivo de configuração foi salvo em {CONFIG_FILE}.")
    except Exception as e:
        print(f"{Fore.RED}[ERRO] Falha ao configurar o comando global: {e}")

def update_autorecon_path():
    print(f"{Fore.YELLOW}Iniciando atualização do caminho do 'autorecon'...")

    try:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../autorecon.py"))
        print(f"{Fore.CYAN}Caminho identificado: {script_path}")

        with open("autorecon_path.conf", "w") as conf:
            conf.write(script_path)
        print(f"{Fore.GREEN}Arquivo 'autorecon_path.conf' criado com sucesso no diretório atual.")
    except Exception as e:
        print(f"{Fore.RED}[ERRO] Falha ao criar o arquivo de configuração: {e}")

