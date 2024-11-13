# Função para verificar se o projeto está dentro de um repositório Git
import subprocess
import sys

def is_git_repo():
    try:
        subprocess.check_call(['git', 'rev-parse', '--is-inside-work-tree'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Função para atualizar o repositório
def update_repository():
    if not is_git_repo():
        print("[ERROR] O script não está sendo executado dentro de um repositório Git.")
        sys.exit(1)
    
    print("Verificando atualizações no repositório...")
    try:
        # Certifique-se de que o repositório está limpo antes de puxar as mudanças
        subprocess.check_call(['git', 'fetch'])
        subprocess.check_call(['git', 'pull'])
        print("Código atualizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falha ao atualizar o repositório: {e}")
        sys.exit(1)
