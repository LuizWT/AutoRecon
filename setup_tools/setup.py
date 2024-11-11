# Bibliotecas e Dependências:
import os
from colorama import init, Fore
import subprocess
from functions.clear_terminal import clear_terminal

# Inicialização:
init(autoreset=True)

# Estruturas de configurações de ferramentas e dependências:
TOOLS_CONFIG = {
    "nmap": {
        "check_command": ["nmap", "--version"],
        "install_commands": {
            "debian": "sudo apt-get update && sudo apt-get install -y nmap",
            "redhat": "sudo dnf install -y nmap",
            "arch": "sudo pacman -Syu --noconfirm nmap",
            "suse": "sudo zypper refresh && sudo zypper install -y nmap"
        }
    },
    "wpscan": {
        "check_command": ["wpscan", "--version"],
        "install_commands": {
            "ruby_required": True,  # WPScan depende de Ruby
            "install_script": "sudo gem install wpscan"
        }
    },
    "sniper": {
        "check_command": ["sudo", "sniper"],
        "install_commands": {
            "git_clone": "https://github.com/1N3/Sn1per",
            "install_script": "cd Sn1per && sudo bash install.sh"
        }
    },
    "ruby": {
        "check_command": ["ruby", "--version"],
        "install_commands": {
            "debian": "sudo apt-get update && sudo apt-get install -y ruby",
            "redhat": "sudo dnf install -y ruby",
            "arch": "sudo pacman -Syu --noconfirm ruby",
            "suse": "sudo zypper refresh && sudo zypper install -y ruby"
        },
        "min_version": "3.0.0"
    },
    "proxychains": {
        "check_command": ["proxychains4", "true"],
        "install_commands": {
            "debian": "sudo apt-get update && sudo apt-get install -y proxychains-ng",
            "redhat": "sudo dnf install -y proxychains-ng",
            "arch": "sudo pacman -Syu --noconfirm proxychains-ng",
            "suse": "sudo zypper refresh && sudo zypper install -y proxychains-ng"
        }
    },
    "go": {
        "check_command": ["go", "version"],
        "install_commands": {
            "debian": "sudo apt-get update && sudo apt-get install -y golang",
            "redhat": "sudo dnf install -y golang-bin",
            "arch": "sudo pacman -Syu --noconfirm go",
            "suse": "sudo zypper refresh && sudo zypper install -y go"
        }
    },
    "nuclei": {
        "check_command": ["nuclei", "--version"],
        "install_commands": {
            "go_required": True,  # Nuclei depende de Go
            "install_script": """
                USER_HOME=$(eval echo ~$SUDO_USER) &&
                cd $USER_HOME && 
                rm -rf nuclei && 
                sudo -u $SUDO_USER git clone https://github.com/projectdiscovery/nuclei.git && 
                cd nuclei && 
                sudo -u $SUDO_USER git config --global --add safe.directory $USER_HOME/nuclei && 
                sudo -u $SUDO_USER mkdir -p $USER_HOME/nuclei/bin && 
                sudo -u $SUDO_USER go build -v -buildvcs=false -o $USER_HOME/nuclei/bin/nuclei ./cmd/nuclei && 
                if [ -n "$BASH_VERSION" ]; then 
                    echo 'export PATH=$PATH:$USER_HOME/nuclei/bin' >> $USER_HOME/.bashrc; 
                elif [ -n "$ZSH_VERSION" ]; then 
                    echo 'export PATH=$PATH:$USER_HOME/nuclei/bin' >> $USER_HOME/.zshrc; 
                fi &&
                sudo cp $USER_HOME/nuclei/bin/nuclei /usr/local/bin/nuclei
            """
        }

    },
    "nikto": {
        "check_command": ["nikto", "-Version"],
        "install_commands": {
            "git_clone": "https://github.com/sullo/nikto",
            "link_script": "cd nikto/program && sudo ln -s $(pwd)/nikto.pl /usr/local/bin/nikto"
        }
    }
}

# Funções de Verificação de Ferramenta:
def check_tool(tool):
    tool_config = TOOLS_CONFIG.get(tool)
    if not tool_config:
        print(f"{Fore.RED}[ERROR] Configuração para {tool} não encontrada.")
        return False

    try:
        if "min_version" in tool_config:
            result = subprocess.run(tool_config["check_command"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            version_output = result.stdout.decode().split()[1]
            return version_output >= tool_config["min_version"]
        else:
            subprocess.run(tool_config["check_command"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{Fore.CYAN}[INFO] {tool.capitalize()} já está instalado.")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}[INFO] {tool.capitalize()} não está instalado.")
        return False


# Funções de Instalação de Ferramenta:
def install_tool(tool):
    tool_config = TOOLS_CONFIG.get(tool)
    if not tool_config:
        print(f"{Fore.RED}[ERROR] Configuração para {tool} não encontrada.")
        return

    try:
        print(f"{Fore.CYAN}[INFO] Iniciando a instalação do {tool.capitalize()}...")

        if "debian_version" in os.listdir("/etc"):
            command = tool_config["install_commands"].get("debian")
        elif "redhat-release" in os.listdir("/etc"):
            command = tool_config["install_commands"].get("redhat")
        elif "arch-release" in os.listdir("/etc"):
            command = tool_config["install_commands"].get("arch")
        elif "SuSE-release" in os.listdir("/etc"):
            command = tool_config["install_commands"].get("suse")
        else:
            print(f"{Fore.RED}[ERROR] Distribuição não suportada para a instalação de {tool}.")
            return

        if "git_clone" in tool_config["install_commands"]:
            os.system(f"git clone {tool_config['install_commands']['git_clone']}")

        if command:
            os.system(command)

        if "install_script" in tool_config["install_commands"]:
            os.system(tool_config["install_commands"]["install_script"])

        if "link_script" in tool_config["install_commands"]:
            os.system(tool_config["install_commands"]["link_script"])
        
        clear_terminal()
        print(f"{Fore.CYAN}[INFO] {tool.capitalize()} instalado com sucesso.")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] Ocorreu um erro durante a instalação de {tool.capitalize()}: {e}")

# Função específica de ProxyChains:
def check_proxychains():
    try:
        subprocess.run(['proxychains4', 'true'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.CYAN}[INFO] ProxyChains já está instalado.")
        return True
    except FileNotFoundError:
        print(f"{Fore.RED}[INFO] ProxyChains não está instalado.")
        return False
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}[INFO] ProxyChains não está funcionando corretamente.")
        return False
