#!/usr/bin/env bash
set -euo pipefail
trap 'echo -e "\e[31m[ERRO]\e[0m Um erro inesperado ocorreu." >&2' ERR

# Cores ANSI
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
NC='\e[0m'
BLUE='\e[34m'

echo -e "${BLUE}========================================="
echo -e "${BLUE}==      AutoRecon - Installer          =="
echo -e "${BLUE}========================================="
echo -e "${YELLOW}+ -- --=[ https://github.com/LuizWT/ ${NC}"

die() {
  echo -e "${RED}[ERROR] $*${NC}" >&2
  exit 1
}

info() {
  echo -e "${GREEN}[OK] $*${NC}"
}

warn() {
  echo -e "${YELLOW}[INFO] $*${NC}"
}

# Detecta gerenciador de pacotes
detect_pm() {
  if command -v apt &>/dev/null; then
    PM='apt'
  elif command -v dnf &>/dev/null; then
    PM='dnf'
  elif command -v pacman &>/dev/null; then
    PM='pacman'
  elif command -v zypper &>/dev/null; then
    PM='zypper'
  else
    die "Gerenciador de pacotes não suportado."
  fi
}

# Instala pacote se necessário
install_pkg() {
  local pkg="$1"
  if ! command -v "$pkg" &>/dev/null; then
    warn "Instalando $pkg..."
    case "$PM" in
      apt)
        sudo apt update && sudo apt install -y "$pkg";;
      dnf)
        sudo dnf install -y "$pkg";;
      pacman)
        sudo pacman -Sy --noconfirm "$pkg";;
      zypper)
        sudo zypper refresh && sudo zypper install -y "$pkg";;
    esac
  else
    info "$pkg já instalado."
  fi
}

# Verifica o venv
check_venv() {
  if ! python3 -m venv --help &>/dev/null; then
    warn "Módulo venv não detectado."
    case "$PM" in
      apt|zypper)
        warn "Instalando pacote de venv para $PM..."
        pkg="${PM == 'apt' && echo python3-venv || echo python3-virtualenv}" # zypper usa python3-virtualenv
        sudo $PM install -y "$pkg"
        ;;  
      *)
        warn "Assumindo que o venv já está incluso no pacote python3 do sistema."
        ;;  
    esac
    python3 -m venv --help &>/dev/null || die "Falha ao habilitar módulo venv."
  else
    info "Módulo venv disponível." 
  fi
}

main() {
  local DEST_DIR="${1:-$HOME/AutoRecon}"

  detect_pm
  install_pkg git
  install_pkg python3
  install_pkg python3-venv
  install_pkg python3-pip
  check_venv

  if [ -d "$DEST_DIR" ]; then
    info "Repositório já clonado em $DEST_DIR"
  else
    warn "Clonando AutoRecon em $DEST_DIR"
    git clone https://github.com/LuizWT/AutoRecon.git "$DEST_DIR"
  fi

  cd "$DEST_DIR"
  info "Criando venv em venv/"
  python3 -m venv venv

  warn "Ativando venv"

  source venv/bin/activate

  [ -s requirements.txt ] || die "requirements.txt não encontrado."
  warn "Instalando dependências..."
  pip install -r requirements.txt

  warn "Executando AutoRecon..."
  sudo venv/bin/python3 autorecon.py

  echo -e "${GREEN}[OK] Tudo pronto! =)${NC}"
  echo "Use: 'source $DEST_DIR/venv/bin/activate' para reativar o ambiente virtual."
}

main "$@"
