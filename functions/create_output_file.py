import os
from colorama import init, Fore
from functions.clear_terminal import clear_terminal
from configurations.ar_updater import get_git_repo_path
import asyncio

init(autoreset=True)

def create_output_file(script_name):
    output_dir = "output"
    output_file = os.path.join(output_dir, f"{script_name}_output.txt")
    os.makedirs(output_dir, exist_ok=True)
    return output_file

def get_project_root():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    repo_path = get_git_repo_path(start_path=script_path)
    if not repo_path:
        raise FileNotFoundError("[ERROR] Diretório raiz do projeto não encontrado.")
    return repo_path

def execute_command_and_log(command, script_name):
    try:

        project_root = get_project_root()

        output_dir = os.path.join(project_root, "output")
        output_file = os.path.join(output_dir, f"{script_name}_output.txt")

        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'a') as f:
            f.write(f"\n\n\nExecutando comando: {command}\n")
        
        print(f"{Fore.YELLOW}Executando comando: {command}")

        result = os.system(command + f" >> {output_file} 2>&1")

        clear_terminal()
        print(f"{Fore.GREEN}Resultados salvos em: {output_file}")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] Falha ao executar comando: {e}")


async def execute_command_and_log_submenu(command, tool_name):
    try:
        project_root = get_project_root()

        output_dir = os.path.join(project_root, "output")
        output_file = os.path.join(output_dir, f"{tool_name}_output.txt")

        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'a') as f:
            f.write(f"\n\n\nExecutando comando: {command}\n")

        full_command = f"{command} >> {output_file} 2>&1"
        print(f"{Fore.YELLOW}Executando comando: {full_command}")

        process = await asyncio.create_subprocess_shell(
            full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Captura a saída e escreve no arquivo de log
        stdout, stderr = await process.communicate()
        with open(output_file, 'a') as f:
            if stdout:
                f.write(stdout.decode())
            if stderr:
                f.write(stderr.decode())

        clear_terminal()
        print(f"{Fore.GREEN}Resultados salvos em: {output_file}")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] Falha ao executar comando: {e}")

