#!/bin/bash
# Caminhos base
LAUNCHER_DIR="$(dirname "$(realpath "$0")")"
PROJECT_DIR="$(dirname "$LAUNCHER_DIR")"
ICON_PATH="$LAUNCHER_DIR/icons/autorecon.png"
DESKTOP_TEMPLATE_FILE="$LAUNCHER_DIR/autorecon.desktop"
LOCAL_DESKTOP_FILE="$HOME/.local/share/applications/autorecon.desktop"
LOCAL_ICON_DIR="$HOME/.local/share/icons"

log_info() { echo "[INFO] $1"; }
log_warn() { echo "[AVISO] $1"; }
log_error() { echo "[ERRO] $1" >&2; exit 1; }

log_info "Verificando pré-requisitos..."

# Verifica o ambiente gráfico
if [ -z "$XDG_CURRENT_DESKTOP" ]; then
    log_warn "Ambiente gráfico não detectado. Arquivos .desktop podem não ser suportados."
elif [[ "$XDG_CURRENT_DESKTOP" =~ "KDE"|"GNOME"|"XFCE"|"LXDE"|"MATE"|"Cinnamon"|"Hyprland" ]]; then
    log_info "Ambiente gráfico detectado: $XDG_CURRENT_DESKTOP."
else
    log_warn "Ambiente gráfico '$XDG_CURRENT_DESKTOP' não testado. Proceda com cautela."
fi

# Garante que o diretório de atalhos exista
mkdir -p "$HOME/.local/share/applications" || log_error "Falha ao criar o diretório de atalhos."

# Verifica a disponibilidade do update-desktop-database
if ! command -v update-desktop-database &>/dev/null; then
    log_error "O comando 'update-desktop-database' não foi encontrado. Por favor, instale-o. Ex: sudo apt install desktop-file-utils (Debian/Ubuntu) ou sudo dnf install desktop-file-utils (Fedora)."
fi

log_info "Criando lançador do AutoRecon..."

# Valida a existência do ícone e do template .desktop
[ ! -f "$ICON_PATH" ] && log_error "Ícone não encontrado em $ICON_PATH"
[ ! -f "$DESKTOP_TEMPLATE_FILE" ] && log_error "Modelo do arquivo .desktop não encontrado em $DESKTOP_TEMPLATE_FILE"

# Cria o arquivo .desktop localmente
sed "s|{PROJECT_DIR}|$PROJECT_DIR|g" "$DESKTOP_TEMPLATE_FILE" > "$LOCAL_DESKTOP_FILE" || log_error "Falha ao criar o arquivo .desktop local."

# Copia o ícone para o diretório de ícones local
mkdir -p "$LOCAL_ICON_DIR" || log_error "Falha ao criar o diretório de ícones local."
cp "$ICON_PATH" "$LOCAL_ICON_DIR/" || log_error "Falha ao copiar o ícone."

# Atualiza o banco de dados de atalhos
update-desktop-database "$HOME/.local/share/applications" || log_error "Falha ao atualizar o banco de dados de atalhos."

log_info "Lançador criado com sucesso!"
log_info "Agora você pode buscar por 'AutoRecon' no menu do sistema."

