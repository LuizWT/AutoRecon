#!/bin/bash
# Caminhos base
LAUNCHER_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(dirname "$LAUNCHER_DIR")"
ICON_PATH="$LAUNCHER_DIR/icons/autorecon.png"
DESKTOP_FILE="$LAUNCHER_DIR/autorecon.desktop"
LOCAL_DESKTOP="$HOME/.local/share/applications/autorecon.desktop"

echo "Criando lançador do AutoRecon..."

if [ ! -f "$ICON_PATH" ]; then
    echo "Ícone não encontrado em $ICON_PATH"
    exit 1
fi

if [ ! -f "$DESKTOP_FILE" ]; then
    echo "Modelo do arquivo .desktop não encontrado em $DESKTOP_FILE"
    exit 1
fi

# Substitui os caminhos no modelo do .desktop
sed "s|{PROJECT_DIR}|$PROJECT_DIR|g" "$DESKTOP_FILE" > "$LOCAL_DESKTOP"

chmod +x "$PROJECT_DIR/launcher/launch_autorecon.sh"

mkdir -p "$HOME/.local/share/icons"
cp "$ICON_PATH" "$HOME/.local/share/icons/"

update-desktop-database "$HOME/.local/share/applications"

echo "Lançador criado com sucesso!"
echo "Agora você pode buscar por 'AutoRecon' no menu do sistema."
