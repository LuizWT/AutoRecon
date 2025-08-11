#!/bin/bash
AUTORECON_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

# Funções de log
log_info() { echo "[INFO] $1"; }
log_error() { echo "[ERRO] $1" >&2; exit 1; }

log_info "Iniciando AutoRecon..."

TERMINALS=(
    "gnome-terminal -- bash -c \"cd '$AUTORECON_DIR' && sudo python3 autorecon.py\""
    "konsole --noclose -e bash -c \"cd '$AUTORECON_DIR' && sudo python3 autorecon.py\""
    "xfce4-terminal -e \"bash -c 'cd '$AUTORECON_DIR' && sudo python3 autorecon.py'\""
    "alacritty -e bash -c \"cd '$AUTORECON_DIR' && sudo python3 autorecon.py\""
    "kitty --hold bash -c \"cd '$AUTORECON_DIR' && sudo python3 autorecon.py\""
    "tilix -e \"bash -c 'cd '$AUTORECON_DIR' && sudo python3 autorecon.py'\""
    "lxterminal -e \"bash -c 'cd '$AUTORECON_DIR' && sudo python3 autorecon.py'\""
    "terminator -e \"bash -c 'cd '$AUTORECON_DIR' && sudo python3 autorecon.py'\""
    "xterm -e \"bash -c 'cd '$AUTORECON_DIR' && sudo python3 autorecon.py'\""
)

LAUNCHED=false
for cmd in "${TERMINALS[@]}"; do
    # Extrai o nome do comando (primeira palavra antes do espaço)
    TERMINAL_CMD=$(echo "$cmd" | awk '{print $1}')

    if command -v "$TERMINAL_CMD" &>/dev/null; then
        log_info "Terminal compatível encontrado: $TERMINAL_CMD. Lançando AutoRecon..."
        eval "$cmd"
        LAUNCHED=true
        break
    fi
done

if [ "$LAUNCHED" = false ]; then
    log_error "Nenhum terminal compatível foi encontrado. Por favor, instale um dos seguintes: gnome-terminal, konsole, xfce4-terminal, alacritty, kitty, tilix, lxterminal, terminator, xterm."
fi