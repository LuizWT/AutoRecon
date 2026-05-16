#!/bin/bash

LOCAL_DESKTOP_FILE="$HOME/.local/share/applications/autorecon.desktop"
LOCAL_ICON_FILE="$HOME/.local/share/icons/autorecon.png"

log_info()  { echo "[INFO] $1"; }
log_warn()  { echo "[AVISO] $1"; }
log_error() { echo "[ERRO] $1" >&2; exit 1; }

removed=0

if [ -f "$LOCAL_DESKTOP_FILE" ]; then
    rm "$LOCAL_DESKTOP_FILE" || log_error "Falha ao remover $LOCAL_DESKTOP_FILE"
    log_info "Arquivo .desktop removido."
    removed=1
else
    log_warn "Arquivo .desktop não encontrado. Lançador pode já ter sido removido."
fi

if [ -f "$LOCAL_ICON_FILE" ]; then
    rm "$LOCAL_ICON_FILE" || log_error "Falha ao remover $LOCAL_ICON_FILE"
    log_info "Ícone removido."
    removed=1
else
    log_warn "Ícone não encontrado."
fi

if [ "$removed" -eq 1 ]; then
    if command -v update-desktop-database &>/dev/null; then
        update-desktop-database "$HOME/.local/share/applications"
    fi
    log_info "Lançador removido com sucesso."
fi
