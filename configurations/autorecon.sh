#!/bin/bash

# Verificações de pré-requisitos
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "Erro: $1 não está instalado. Instale-o e tente novamente."
        exit 1
    fi
}

echo "Verificando dependências do sistema..."

check_command git
check_command python3
check_command pip3

# Verifica o VENV isoladamente
if ! python3 -m venv --help &> /dev/null; then
    echo "Erro: O módulo venv do Python não está disponível. Instale com:"
    echo "Debian/Ubuntu: sudo apt install python3-venv"
    echo "Fedora: sudo dnf install python3-venv"
    echo "Arch: sudo pacman -S python-virtualenv"
    exit 1
fi

# Define o diretório de destino
DEST_DIR="$HOME/AutoRecon"

# Valida se o repo já está clonado e, caso não esteja, o clona
if [ -d "$DEST_DIR" ]; then
    echo "O diretório $DEST_DIR já existe."
else
    echo "Clonando o AutoRecon para $DEST_DIR..."
    git clone https://github.com/LuizWT/AutoRecon.git "$DEST_DIR"
    if [ $? -ne 0 ]; then
        echo "Erro ao clonar o repositório."
        exit 1
    fi
fi

# Entra no diretório
cd "$DEST_DIR" || {
    echo "Erro ao entrar no diretório $DEST_DIR."
    exit 1
}

# Cria o VENV
echo "Criando ambiente virtual em venv/..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Erro ao criar o ambiente virtual com python3."
    exit 1
fi

# Usa o source para ativar o VENV
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Erro ao ativar o ambiente virtual."
    exit 1
fi

# Instala as dependências
echo "Instalando dependências do requirements.txt..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Erro ao instalar as dependências."
    deactivate
    exit 1
fi

# Executa o autorecon com o caminho do python3 do ambiente VENV (previne erro)
echo "Executando autorecon.py com sudo..."
sudo venv/bin/python3 autorecon.py

echo "Instalação e verificação concluídas com sucesso!"
