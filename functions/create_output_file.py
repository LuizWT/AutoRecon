from pathlib import Path
import os
from colorama import init, Fore
from functions.clear_terminal import clear_terminal
from configurations.ar_updater import get_git_repo_path
import asyncio

init(autoreset=True)

def create_output_file(script_name):
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{script_name}_output.txt"


def get_project_root():
    script_path = Path(__file__).resolve().parent
    repo_path = get_git_repo_path(start_path=script_path)
    if not repo_path:
        raise FileNotFoundError("[ERROR] Diretório raiz do projeto não encontrado.")
    return repo_path

def execute_command_and_log(command, script_name):
    try:
        project_root = get_project_root()
        output_dir = project_root / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{script_name}_output.txt"

        with output_file.open('a') as f:
            f.write(f"\n\n\nExecutando comando: {command}\n")

        print(f"{Fore.YELLOW}Executando comando: {command}")
        os.system(f"{command} >> {output_file} 2>&1")
        clear_terminal()
        print(f"{Fore.GREEN}Resultados salvos em: {output_file}")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] Falha ao executar comando: {e}")


async def execute_command_and_log_submenu(command, tool_name):
    try:
        project_root = get_project_root()
        output_dir = project_root / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{tool_name}_output.txt"

        with output_file.open('a') as f:
            f.write(f"\n\n\nExecutando comando: {command}\n")

        full_command = f"{command} >> {output_file} 2>&1"
        print(f"{Fore.YELLOW}Executando comando: {full_command}")

        process = await asyncio.create_subprocess_shell(
            full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        with output_file.open('a') as f:
            if stdout:
                f.write(stdout.decode())
            if stderr:
                f.write(stderr.decode())

        clear_terminal()
        print(f"{Fore.GREEN}Resultados salvos em: {output_file}")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] Falha ao executar comando: {e}")

