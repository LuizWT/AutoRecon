import os
import stat
import subprocess
from colorama import Fore, init

init(autoreset=True)

def configure_global_command():
    script_name = "autorecon"
    target_path = f"/usr/local/bin/{script_name}"

    # Caminho fixo para o autorecon.py, no diretório raiz do projeto
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../autorecon.py"))

    # Verificar se o comando já está configurado em /usr/local/bin
    if os.path.exists(target_path):
        print(f"{Fore.YELLOW}O comando '{script_name}' já está configurado em {target_path}.")
        return

    # Criar o conteúdo do script
    shell_script_content = f"#!/bin/bash\nsudo python3 {script_path} \"$@\""

    try:
        # Criar o arquivo temporário do shell script
        with open(script_name, "w") as f:
            f.write(shell_script_content)

        # Tornar o arquivo executável
        os.chmod(script_name, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

        # Mover o script para /usr/local/bin com privilégios de root
        subprocess.run(["sudo", "mv", script_name, target_path], check=True)
        print(f"{Fore.GREEN}Comando '{script_name}' configurado com sucesso em {target_path}. Agora você pode executá-lo usando 'sudo {script_name}'.")

    except Exception as e:
        print(f"{Fore.RED}[ERRO] Falha ao configurar o comando global: {e}")
