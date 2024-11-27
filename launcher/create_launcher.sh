#!/bin/bash
# Caminhos base
LAUNCHER_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(dirname "$LAUNCHER_DIR")"
ICON_PATH="$LAUNCHER_DIR/icons/autorecon.png"
DESKTOP_FILE="$LAUNCHER_DIR/autorecon.desktop"
LOCAL_DESKTOP="$HOME/.local/share/applications/autorecon.desktop"

echo "Verificando pré-requisitos..."

# Verifica o ambiente gráfico
if [ -z "$XDG_CURRENT_DESKTOP" ]; then
    echo "Aviso: Ambiente gráfico não detectado. Arquivos .desktop podem não ser suportados."
elif [[ "$XDG_CURRENT_DESKTOP" =~ "KDE"|"GNOME"|"XFCE"|"LXDE"|"MATE"|"Cinnamon"|"Hyprland" ]]; then
    echo "Ambiente gráfico detectado: $XDG_CURRENT_DESKTOP."
else
    echo "Aviso: Ambiente gráfico '$XDG_CURRENT_DESKTOP' não testado. Proceda com cautela."
fi

# Verifica os diretórios padrões para atalhos
if [ ! -d "$HOME/.local/share/applications" ]; then
    echo "Diretório de atalhos não encontrado. Criando..."
    mkdir -p "$HOME/.local/share/applications" || {
        echo "Erro ao criar o diretório de atalhos. Saindo."
        exit 1
    }
fi

if ! command -v update-desktop-database &>/dev/null; then
    echo "O comando 'update-desktop-database' não foi encontrado. Considere instalá-lo."
    echo "Exemplo no Fedora: sudo dnf install desktop-file-utils"
    echo "Exemplo no Ubuntu: sudo apt install desktop-file-utils"
    exit 1
fi

echo "Criando lançador do AutoRecon..."

if [ ! -f "$ICON_PATH" ]; then
    echo "Ícone não encontrado em $ICON_PATH"
    exit 1
fi

if [ ! -f "$DESKTOP_FILE" ]; then
    echo "Modelo do arquivo .desktop não encontrado em $DESKTOP_FILE"
    exit 1
fi

sed "s|{PROJECT_DIR}|$PROJECT_DIR|g" "$DESKTOP_FILE" > "$LOCAL_DESKTOP"

mkdir -p "$HOME/.local/share/icons"
cp "$ICON_PATH" "$HOME/.local/share/icons/"

update-desktop-database "$HOME/.local/share/applications"

echo "Lançador criado com sucesso!"
echo "Agora você pode buscar por 'AutoRecon' no menu do sistema."
