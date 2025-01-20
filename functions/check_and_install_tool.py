from colorama import Fore, init
from functions.clear_terminal import clear_terminal
from setup_tools.setup import TOOLS_CONFIG, install_tool
import subprocess

init(autoreset=True)

def check_min_version(tool_name, min_version):
    try:
        result = subprocess.run(TOOLS_CONFIG[tool_name]["check_command"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        version_output = result.stdout.decode().split()[1]
        return version_output >= min_version
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"{Fore.RED}[ERROR] Falha ao verificar a versão de {tool_name}: {e}")
        return False

async def check_and_install_tool(tool_name, menu_func, global_target):
    tool_config = TOOLS_CONFIG.get(tool_name)
    if not tool_config:
        print(f"{Fore.RED}[ERROR] Configuração para {tool_name} não encontrada.")
        return
    
    print(f"{Fore.GREEN}[INFO] Verificando a instalação do {tool_name}...")
    
    try:
        if "min_version" in tool_config:
            is_installed = check_min_version(tool_name, tool_config["min_version"])
        else:
            is_installed = subprocess.run(tool_config["check_command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
    except FileNotFoundError:
        is_installed = False

    if is_installed:
        print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")

        await menu_func(global_target)
        
    else:
        if tool_config.get("install_commands"):
            install_commands = tool_config["install_commands"]

            # Verifica se há a dependencia de Ruby
            if install_commands.get("ruby_required"):
                try:
                    subprocess.run(TOOLS_CONFIG["ruby"]["check_command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except FileNotFoundError:
                    install_dep = input(f"{Fore.YELLOW}[INFO] {tool_name} requer Ruby.\nDeseja instalar Ruby e {tool_name}? (y/n): ").lower()
                    if install_dep in ['s', 'y']:
                        install_tool("ruby")
                        install_tool(tool_name)
                        is_installed =  True
                        print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")
                        await menu_func(global_target)
                    else:
                        print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
                        return
                        
            # Verifica se há a dependencia de Go
            if install_commands.get("go_required"):
                try:
                    subprocess.run(TOOLS_CONFIG["go"]["check_command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except FileNotFoundError:
                    install_dep = input(f"{Fore.YELLOW}[INFO] {tool_name} requer Go.\nDeseja instalar Go e {tool_name}? (y/n): ").lower()
                    if install_dep in ['s', 'y']:
                        install_tool("go")
                        install_tool(tool_name)
                        is_installed = True
                        print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")
                        await menu_func(global_target)
                    else:
                        print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
                        return
                    
            if install_commands.get("docker_required"):
                try:
                    subprocess.run(TOOLS_CONFIG["docker"]["check_command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                except FileNotFoundError:
                    install_dep = input(f"{Fore.YELLOW}[INFO] {tool_name} requer Docker.\nDeseja instalar Docker e {tool_name}? (y/n): ").lower()
                    if install_dep in ['s', 'y']:
                        install_tool("docker")
                        install_tool(tool_name)
                        is_installed = True
                        print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")
                        await menu_func(global_target)
                    else:
                        print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
                        return

        if is_installed == False:
            install_choice = input(f"{Fore.YELLOW}[INFO] {tool_name} não está instalado. Deseja instalar o {tool_name}? (y/n): ").lower()
            if install_choice in ['s', 'y']:
                install_tool(tool_name)
                print(f"{Fore.GREEN}[INFO] Abrindo o menu {tool_name.upper()}...")

                await menu_func(global_target)
            else:
                print(f"{Fore.RED}[INFO] Retornando ao menu principal...")
