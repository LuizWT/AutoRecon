#!/usr/bin/env python3
import os
import stat
import subprocess
from pathlib import Path
from colorama import Fore, init

init(autoreset=True)

CONFIG_FILE = Path("/etc/autorecon_path.conf")
SCRIPT_NAME = "autorecon"
TARGET_PATH = Path(f"/usr/local/bin/{SCRIPT_NAME}")

def _get_script_path() -> Path:
    # Diretório absoluto do script
    return (Path(__file__).resolve().parent.parent / "autorecon.py").resolve()

def _run_command(cmd: list[str], error_msg: str) -> None:
    # Executa um comando e trata erros
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[ERRO] {error_msg}: {e.stderr.strip()}")
        raise
    except Exception as e:
        print(f"{Fore.RED}[ERRO] {error_msg}: {e}")
        raise

def configure_global_command(force: bool = False, backup: bool = True) -> None:
    # Configura o alias 'autorecon' e o .conf

    # Ignora se já existir
    if TARGET_PATH.exists() and not force:
        return

    print(f"{Fore.YELLOW}Configurando o comando global '{SCRIPT_NAME}'...")

    script_path = _get_script_path()

    # Script bash que redireciona para o autorecon.py
    launcher_content = f"""#!/bin/bash
        if [ -f {CONFIG_FILE} ]; then
            script_path=$(cat {CONFIG_FILE})
            if [ -f "$script_path" ]; then
                sudo python3 "$script_path" "$@"
            else
                echo "[ERROR]: O arquivo $script_path não foi encontrado."
                echo "Atualize o diretório em: sudo nano {CONFIG_FILE}"
            fi
        else
            echo "[ERROR]: Arquivo de configuração {CONFIG_FILE} não encontrado."
            echo "Reconfigure o 'autorecon' e atualize o diretório em: sudo nano {CONFIG_FILE}"
        fi
    """

    try:
        # Criar o launcher temporário
        tmp_launcher = Path(f"./{SCRIPT_NAME}")
        tmp_launcher.write_text(launcher_content)
        tmp_launcher.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

        # Mover para /usr/local/bin
        _run_command(["sudo", "mv", str(tmp_launcher), str(TARGET_PATH)],
                     f"Falha ao mover o script '{SCRIPT_NAME}' para {TARGET_PATH}")

        # Cria e move o arquivo de configuração
        tmp_conf = Path(f"./{SCRIPT_NAME}_path.conf")
        tmp_conf.write_text(str(script_path))
        _run_command(["sudo", "mv", str(tmp_conf), str(CONFIG_FILE)],
                     f"Falha ao mover o arquivo de configuração para {CONFIG_FILE}")

        print(f"{Fore.GREEN}Comando '{SCRIPT_NAME}' configurado com sucesso em {TARGET_PATH}.")
        print(f"{Fore.GREEN}O arquivo de configuração foi salvo em {CONFIG_FILE}.")
    except Exception:
        print(f"{Fore.RED}[ERRO] Falha geral ao configurar o comando global.")

def update_autorecon_path() -> None:
    # Atualiza o caminho do script principal no arquivo de configuração
    print(f"{Fore.YELLOW}Atualizando caminho do '{SCRIPT_NAME}'...")
    script_path = _get_script_path()
    print(f"{Fore.CYAN}Caminho identificado: {script_path}")

    try:
        CONFIG_FILE.write_text(str(script_path))
        print(f"{Fore.GREEN}Caminho do '{SCRIPT_NAME}' atualizado com sucesso em {CONFIG_FILE}.")
    except Exception as e:
        print(f"{Fore.RED}[ERRO] Falha ao atualizar o arquivo de configuração: {e}")
