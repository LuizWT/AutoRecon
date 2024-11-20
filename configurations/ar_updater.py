import os
import subprocess
import argparse
import sys
from colorama import Fore, init

init(autoreset=True)

def is_git_repo(path):
    try:
        subprocess.check_call(['git', 'rev-parse', '--is-inside-work-tree'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=path)
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_repo_path(start_path=None):
    if start_path is None:
        start_path = os.getcwd()

    while os.path.exists(os.path.join(start_path, '.git')):
        return start_path
    
    parent_dir = os.path.dirname(start_path)
    if parent_dir == start_path:
        return None
    return get_git_repo_path(parent_dir)

# Função para atualizar o repositório
def update_repository():

    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../autorecon.py"))
    repo_path = get_git_repo_path(start_path=os.path.dirname(script_path))

    if not repo_path:
        print("[ERROR] O script não está sendo executado dentro de um repositório Git.")
        sys.exit(1)

    print(f"Verificando atualizações no repositório localizado em: {repo_path}")

    # Verifica se o repositório Git é válido
    if not is_git_repo(repo_path):
        print(f"[ERROR] '{repo_path}' Não é um repositório Git válido.")
        sys.exit(1)

    try:
        os.chdir(repo_path)

        # Evita erro de propriedade
        subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', repo_path])

        env = os.environ.copy()
        env['GIT_DISCOVERY_ACROSS_FILESYSTEM'] = '1'

        subprocess.run(['sudo', 'git', 'fetch'], check=True, env=env)
        subprocess.run(['sudo', 'git', 'pull'], check=True, env=env)

        print(f"{Fore.GREEN}Código atualizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falha ao atualizar o repositório: {e}")
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="AutoRecon - Ferramenta de Automação de Segurança")
    parser.add_argument('-update', action='store_true', help="Atualiza o código para a versão mais recente")
    return parser.parse_args()

def new_version_checker():
    try:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../autorecon.py"))
        repo_path = get_git_repo_path(start_path=os.path.dirname(script_path))

        if not repo_path:
            print("[ERROR] O script não está sendo executado dentro de um repositório Git.")
            return False

        # Define o diretório de trabalho como o local do script
        os.chdir(repo_path)

        result = subprocess.run(['git', 'fetch'], capture_output=True, text=True)
        if result.returncode != 0:
            return False
        
        # Compara o estado atual do repositório local com o remoto
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True)
        if result.returncode == 0:
            # Se a saída tiver "behind", significa que está desatualizado
            if "behind" in result.stdout:
                return True
            else:
                return False
        else:
            print("[ERROR] Falha ao verificar o status do repositório.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Erro ao verificar commits: {e}")
        return False
