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
            "debian": "sudo apt update && sudo apt install -y nmap",
            "redhat": "sudo dnf install -y nmap",
            "arch": "sudo pacman -Syu --noconfirm nmap",
            "suse": "sudo zypper refresh && sudo zypper install -y nmap"
        }
    },
    "wpscan": {
        "check_command": ["wpscan", "--version"],
        "install_commands": {
            "ruby_required": True,  # Gem WPScan depende de Ruby
            "debian": "sudo gem install wpscan",
            "redhat": "sudo gem install wpscan",
            "suse": "sudo gem install wpscan",
            "arch": "sudo gem install wpscan -n /usr/local/bin"
        }
    },

    "sniper": {
        "check_command": ["sudo", "sniper"],
        "install_commands": {
            "install_script": """
                USER_HOME=$(eval echo ~$SUDO_USER) &&
                cd $USER_HOME &&
                sudo -u $SUDO_USER git clone https://github.com/1N3/Sn1per &&
                cd Sn1per &&
                sudo bash install.sh
            """
        }
    },

    "ruby": {
        "check_command": ["ruby", "--version"],
        "install_commands": {
            "debian": "sudo apt-get update && sudo apt-get install -y ruby",
            "redhat": "sudo dnf install -y ruby && sudo dnf install ruby-devel",
            "arch": "sudo pacman -S base-devel && sudo pacman -S ruby rubygems ruby-erb",
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

                cd $USER_HOME/nuclei && 

                sudo -u $SUDO_USER mkdir -p $USER_HOME/nuclei/bin && 

                sudo -u $SUDO_USER go build -v -buildvcs=false -o $USER_HOME/nuclei/bin/nuclei ./cmd/nuclei && 

                # Adicionando o binário ao PATH
                if [ -n "$BASH_VERSION" ]; then 
                    echo 'export PATH=$PATH:$USER_HOME/nuclei/bin' >> $USER_HOME/.bashrc; 
                    source $USER_HOME/.bashrc;
                elif [ -n "$ZSH_VERSION" ]; then 
                    echo 'export PATH=$PATH:$USER_HOME/nuclei/bin' >> $USER_HOME/.zshrc; 
                    source $USER_HOME/.zshrc;
                fi && 

                sudo cp $USER_HOME/nuclei/bin/nuclei /usr/local/bin/nuclei
            """
        }
    },

    "nikto": {
        "check_command": ["nikto", "-Version"],
        "install_commands": {
            "install_script": """
                cd ~ &&
                sudo rm -rf nikto &&
                git clone https://github.com/sullo/nikto &&
                cd nikto/program &&
                sudo ln -s $(pwd)/nikto.pl /usr/local/bin/nikto
            """
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
    config = TOOLS_CONFIG.get(tool)
    if not config:
        print(f"{Fore.RED}[ERROR] Configuração para {tool} não encontrada.")
        return
    print(f"{Fore.CYAN}[INFO] Instalando {tool}...")
    # Detecta distro apenas uma vez
    distro = None
    if os.path.exists("/etc/debian_version"):
        distro = "debian"
    elif os.path.exists("/etc/redhat-release"):
        distro = "redhat"
    elif os.path.exists("/etc/arch-release"):
        distro = "arch"
    elif os.path.exists("/etc/SuSE-release"):
        distro = "suse"
    if distro is None:
        print(f"{Fore.RED}[ERROR] Distribuição não suportada.")
        return
    # Obtém comando
    command = config["install_commands"].get(distro)
    if not command and "install_script" in config["install_commands"]:
        command = config["install_commands"]["install_script"]
    if not command:
        print(f"{Fore.RED}[ERROR] Nenhum comando de instalação definido para {tool}.")
        return
    try:
        result = subprocess.run(command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(result.stderr.decode())
        clear_terminal()
        print(f"{Fore.CYAN}[INFO] {tool.capitalize()} instalado com sucesso.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Erro na instalação de {tool}: {e}")