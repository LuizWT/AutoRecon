#!/bin/bash
AUTORECON_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

if command -v gnome-terminal &>/dev/null; then
    gnome-terminal -- bash -c "cd $AUTORECON_DIR && sudo python3 autorecon.py; exec bash"
elif command -v konsole &>/dev/null; then
    konsole --noclose -e "cd $AUTORECON_DIR && sudo python3 autorecon.py"
elif command -v xfce4-terminal &>/dev/null; then
    xfce4-terminal -e "bash -c 'cd $AUTORECON_DIR && sudo python3 autorecon.py; exec bash'"
elif command -v alacritty &>/dev/null; then
    alacritty -e bash -c "cd $AUTORECON_DIR && sudo python3 autorecon.py; exec bash"
elif command -v kitty &>/dev/null; then
    kitty bash -c "cd $AUTORECON_DIR && sudo python3 autorecon.py; exec bash"
else
    echo "Nenhum terminal compatível foi encontrado."
    exit 1
fi