import os
import subprocess
import argparse
import sys
from pathlib import Path
from colorama import Fore, init

init(autoreset=True)


def is_git_repo(path: Path) -> bool:
    # fallback simples: basta existir .git
    return (path / '.git').is_dir()

def get_git_repo_path(start_path: Path | None = None) -> Path | None:
    path = start_path or Path.cwd()
    for parent in [path, *path.parents]:
        if (parent / '.git').is_dir():
            return parent
    return None

def update_repository() -> None:
    repo_root = get_git_repo_path(Path.cwd())
    if not repo_root:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Não encontrado repositório Git em {Path.cwd()}")
        sys.exit(1)

    # Só checa git-rev-parse se não for root
    if os.geteuid() != 0 and not is_git_repo(repo_root):
        print(f"{Fore.RED}[ERROR]{Fore.RESET} '{repo_root}' não é um repositório Git válido.")
        sys.exit(1)

    # configura safe.directory (evita “dubious ownership”)
    subprocess.run(
        ['git', 'config', '--global', '--add', 'safe.directory', str(repo_root)],
        check=False
    )

    print(f"Verificando atualizações no repositório localizado em: {repo_root}")

    env = os.environ.copy()
    env['GIT_DISCOVERY_ACROSS_FILESYSTEM'] = '1'
    try:
        subprocess.run(['git', 'fetch'], cwd=repo_root, env=env, check=True)
        subprocess.run(['git', 'pull'], cwd=repo_root, env=env, check=True)
        print(f"{Fore.GREEN}Código atualizado com sucesso.{Fore.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Falha ao atualizar o repositório: {e}")
        sys.exit(1)

def new_version_checker() -> bool:
    # Verifica se o repositório está atrás do remoto (precisa de update), a partir do CWD.
    
    repo_root = get_git_repo_path(Path.cwd())
    if not repo_root:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Não encontrado repositório Git em {Path.cwd()}.")
        return False

    try:
        # Fetch para atualizar referências remotas
        subprocess.run(
            ['git', 'fetch'], cwd=repo_root, capture_output=True, text=True, check=True
        )
        status = subprocess.run(
            ['git', 'status', '-uno'], cwd=repo_root, capture_output=True, text=True, check=True
        )
        return 'behind' in status.stdout
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Erro ao verificar commits: {e}")
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AutoRecon - Ferramenta de Automação de Segurança"
    )
    parser.add_argument(
        '-u', '--update', action='store_true', help="Atualiza o código para a versão mais recente"
    )
    return parser.parse_args()
