from functions.proxy_chains import ProxyManager


def _cmd(*args: str) -> list[str]:
    """Wraps a command with sudo and, if enabled, proxychains."""
    if ProxyManager.is_enabled():
        return ["sudo", "proxychains", *args]
    return ["sudo", *args]


REGISTRY: dict[str, dict] = {
    "nmap": {
        "label": "NMAP",
        "ascii": r"""
        _ __  _ __ ___   __ _ _ __
        | '_ \| '_ ` _ \ / _` | '_ \
        | | | | | | | | | (_| | |_) |
        |_| |_|_| |_| |_|\__,_| .__/
                              | |
                              |_|    """,
        "modes": {
            "target_spec": {
                "label": "VARREDURA PADRÃO",
                "info": "Varre IPs, intervalos, CIDR, arquivos, etc.",
                "build": lambda target, **_: _cmd("nmap", target),
            },
            "scan_technique": {
                "label": "TÉCNICAS DE VARREDURA",
                "info": "Técnicas TCP, UDP, ACK, FIN, NULL, Xmas, etc.",
                "build": lambda target, technique="-sS", **_: _cmd("nmap", technique, target),
            },
            "host_discovery": {
                "label": "DESCOBRIR HOSTS",
                "info": "Descobre hosts ativos na rede.",
                "build": lambda target, **_: _cmd("nmap", "-sn", target),
            },
            "port_spec": {
                "label": "ESPECIFICAÇÃO DE PORTAS",
                "info": "Varre portas específicas ou faixa (ex: 21,22 ou 1-100).",
                "build": lambda target, ports="80", **_: _cmd("nmap", "-p", ports, target),
            },
            "service_detection": {
                "label": "DETECÇÃO DE SERVIÇOS",
                "info": "Detecta serviços e versões em execução.",
                "build": lambda target, **_: _cmd("nmap", "-sV", target),
            },
            "os_detection": {
                "label": "DETECÇÃO DE SO",
                "info": "Tenta identificar o sistema operacional do alvo.",
                "build": lambda target, **_: _cmd("nmap", "-O", target),
            },
            "timing": {
                "label": "TEMPORIZAÇÃO E DESEMPENHO",
                "info": "Ajusta a velocidade da varredura (0 = lento, 5 = rápido).",
                "build": lambda target, level="3", **_: _cmd("nmap", f"-T{level}", target),
            },
            "http_title": {
                "label": "HTTP TITLE",
                "info": "Varre portas 80 e 443 para título HTTP.",
                "build": lambda target, **_: _cmd("nmap", "-p", "80,443", "--script=http-title", target),
            },
            "ssl_cert": {
                "label": "SSL CERT",
                "info": "Varre a porta 443 para certificado SSL.",
                "build": lambda target, **_: _cmd("nmap", "-p", "443", "--script=ssl-cert", target),
            },
            "vuln": {
                "label": "VULN",
                "info": "Varre portas 80 e 443 para vulnerabilidades conhecidas.",
                "build": lambda target, **_: _cmd("nmap", "-p", "80,443", "--script=vuln", target),
            },
            "smb_os_discovery": {
                "label": "SMB OS DISCOVERY",
                "info": "Varre porta 445 para descobrir SO via SMB.",
                "build": lambda target, **_: _cmd("nmap", "-p", "445", "--script=smb-os-discovery", target),
            },
            "http_robots_txt": {
                "label": "HTTP ROBOTS.TXT",
                "info": "Varre portas 80 e 443 para arquivo robots.txt.",
                "build": lambda target, **_: _cmd("nmap", "-p", "80,443", "--script=http-robots.txt", target),
            },
            "ssh_hostkey": {
                "label": "SSH HOSTKEY",
                "info": "Varre a porta 22 para chave do host SSH.",
                "build": lambda target, **_: _cmd("nmap", "-p", "22", "--script=ssh-hostkey", target),
            },
            "dns_brute": {
                "label": "DNS BRUTE FORCE",
                "info": "Realiza força bruta em DNS do domínio alvo.",
                "build": lambda target, **_: _cmd(
                    "nmap", "--script=dns-brute", f"--script-args=dns-brute.domain={target}"
                ),
            },
            "all_commands": {
                "label": "EXECUTAR TODOS OS COMANDOS",
                "info": "Executa todos os modos nmap em sequência.",
                "multi": True,
                "build": lambda target, **_: [
                    _cmd("nmap", "-sS", "-v", target),
                    _cmd("nmap", "-sT", "-v", target),
                    _cmd("nmap", "-sU", "-v", target),
                    _cmd("nmap", "-sF", "-v", target),
                    _cmd("nmap", "-sN", "-v", target),
                    _cmd("nmap", "-sX", "-v", target),
                    _cmd("nmap", "-sn", "-v", target),
                    _cmd("nmap", "-sV", "-v", target),
                    _cmd("nmap", "-O", "-v", target),
                    _cmd("nmap", "-p-", "-v", "--script=http-title", target),
                    _cmd("nmap", "-p", "443", "-v", "--script=ssl-cert", target),
                    _cmd("nmap", "-p-", "-v", "--script=vuln", target),
                    _cmd("nmap", "-p", "445", "-v", "--script=smb-os-discovery", target),
                    _cmd("nmap", "-p-", "-v", "--script=http-robots.txt", target),
                    _cmd("nmap", "-p", "22", "-v", "--script=ssh-hostkey", target),
                    _cmd("nmap", "--script=dns-brute", f"--script-args=dns-brute.domain={target}"),
                ],
            },
        },
    },

    "nuclei": {
        "label": "NUCLEI",
        "ascii": r"""
         _   _            _      _
        | \ | |          | |    (_)
        |  \| |_   _  ___| | ___ _
        | . ` | | | |/ __| |/ _ \ |
        | |\  | |_| | (__| |  __/ |
        |_| \_|\__,_|\___|_|\___|_|""",
        "modes": {
            "target_spec": {
                "label": "VARREDURA PADRÃO",
                "info": "Executa todas as templates no alvo.",
                "build": lambda target, **_: _cmd("nuclei", "-target", target),
            },
            "severity": {
                "label": "FILTRAR POR SEVERIDADE",
                "info": "Filtra resultados por severidade: low, medium, high, critical.",
                "build": lambda target, severity="high", **_: _cmd(
                    "nuclei", "-severity", severity, "-target", target
                ),
            },
            "multi_target": {
                "label": "VARREDURA MÚLTIPLA",
                "info": "Usa arquivo com lista de alvos (um por linha).",
                "build": lambda target_file, **_: _cmd("nuclei", "-targets", target_file),
            },
            "network_scan": {
                "label": "VARREDURA DE REDE",
                "info": "Varredura de rede via CIDR (ex: 192.168.1.0/24).",
                "build": lambda target, **_: _cmd("nuclei", "-target", target),
            },
            "custom_template": {
                "label": "TEMPLATE PERSONALIZADO",
                "info": "Usa template local ou remoto personalizado.",
                "build": lambda target, template="", **_: _cmd("nuclei", "-u", target, "-t", template),
            },
            "dashboard": {
                "label": "ENVIAR PARA PROJECTDISCOVERY",
                "info": "Envia resultados ao dashboard ProjectDiscovery.",
                "build": lambda target, **_: _cmd("nuclei", "-target", target, "-dashboard"),
            },
        },
    },

    "sniper": {
        "label": "SNIPER",
        "ascii": r"""
        _____       _
        /  ___|     (_)
        \ `--. _ __  _ _ __   ___ _ __
         `--. \ '_ \| | '_ \ / _ \ '__|
        /\__/ / | | | | |_) |  __/ |
        \____/|_| |_|_| .__/ \___|_|
                      | |
                      |_|              """,
        "modes": {
            "normal": {
                "label": "MODO PADRÃO",
                "info": "Varredura padrão do Sn1per.",
                "build": lambda target, **_: _cmd("sniper", "-t", target),
            },
            "osint_recon": {
                "label": "OSINT + RECONHECIMENTO",
                "info": "Combina reconhecimento OSINT com varredura.",
                "build": lambda target, **_: _cmd("sniper", "-t", target, "-o", "-re"),
            },
            "stealth": {
                "label": "FURTIVO + OSINT + RECONHECIMENTO",
                "info": "Modo furtivo: combina stealth, OSINT e reconhecimento.",
                "build": lambda target, **_: _cmd("sniper", "-t", target, "-m", "stealth", "-o", "-re"),
            },
            "discover": {
                "label": "MODO DE DESCOBERTA",
                "info": "Descoberta de hosts usando wordlist.",
                "build": lambda target, wordlist="", **_: _cmd(
                    "sniper", "-t", target, "-m", "discover", "-w", wordlist
                ),
            },
            "port": {
                "label": "PORTA ESPECÍFICA",
                "info": "Escaneia somente a(s) porta(s) informadas.",
                "build": lambda target, ports="80", **_: _cmd(
                    "sniper", "-t", target, "-m", "port", "-p", ports
                ),
            },
            "fullportonly": {
                "label": "TODAS AS PORTAS",
                "info": "Escaneia todas as portas abertas.",
                "build": lambda target, **_: _cmd("sniper", "-t", target, "-fp"),
            },
            "web": {
                "label": "MODO WEB",
                "info": "Foco em serviços web (HTTP/HTTPS).",
                "build": lambda target, **_: _cmd("sniper", "-t", target, "-m", "web"),
            },
            "webporthttp": {
                "label": "PORTA HTTP ESPECÍFICA",
                "info": "Escaneia porta HTTP informada.",
                "build": lambda target, ports="80", **_: _cmd(
                    "sniper", "-t", target, "-m", "webporthttp", "-p", ports
                ),
            },
            "webporthttps": {
                "label": "PORTA HTTPS ESPECÍFICA",
                "info": "Escaneia porta HTTPS informada.",
                "build": lambda target, ports="443", **_: _cmd(
                    "sniper", "-t", target, "-m", "webporthttps", "-p", ports
                ),
            },
            "webscan": {
                "label": "VULNERABILIDADES WEB",
                "info": "Varredura de vulnerabilidades em aplicações web.",
                "build": lambda target, **_: _cmd("sniper", "-t", target, "-m", "webscan"),
            },
            "bruteforce": {
                "label": "FORÇA BRUTA",
                "info": "Modo de força bruta em serviços do alvo.",
                "build": lambda target, **_: _cmd("sniper", "-t", target, "-b"),
            },
        },
    },

    "nikto": {
        "label": "NIKTO",
        "ascii": r"""
          _   _ _ _    _
         | \ | (_) |  | |
         |  \| |_| | _| |_ ___
         | . ` | | |/ / __/ _ \
         | |\  | |   <| || (_) |
         |_| \_|_|_|\_\\__\___/ """,
        "modes": {
            "vuln_checks": {
                "label": "VERIFICAÇÕES DE VULNERABILIDADES",
                "info": "Executa todas as verificações de vulnerabilidades.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-C", "all"),
            },
            "server_modules": {
                "label": "VERIFICAÇÕES DE MÓDULOS DO SERVIDOR",
                "info": "Verifica todos os módulos do servidor web.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-M", "all"),
            },
            "config_files": {
                "label": "ARQUIVOS DE CONFIGURAÇÃO",
                "info": "Testa presença de arquivos de configuração sensíveis.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-e", "all"),
            },
            "cookie_security": {
                "label": "SEGURANÇA DE COOKIES",
                "info": "Analisa flags e segurança dos cookies.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-C", "-p"),
            },
            "protocols": {
                "label": "VERIFICAÇÕES DE PROTOCOLOS",
                "info": "Verifica protocolos HTTP disponíveis.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-p"),
            },
            "dir_file_scan": {
                "label": "VARREDURA DE DIRETÓRIOS",
                "info": "Enumera diretórios e arquivos acessíveis.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-d"),
            },
            "third_party_scripts": {
                "label": "SCRIPTS DE TERCEIROS",
                "info": "Detecta scripts e bibliotecas de terceiros.",
                "build": lambda target, **_: _cmd("nikto", "-h", target, "-T"),
            },
            "all_commands": {
                "label": "EXECUTAR TODOS OS COMANDOS",
                "info": "Executa todos os modos nikto em sequência.",
                "multi": True,
                "build": lambda target, **_: [
                    _cmd("nikto", "-h", target, "-C", "all"),
                    _cmd("nikto", "-h", target, "-M", "all"),
                    _cmd("nikto", "-h", target, "-e", "all"),
                    _cmd("nikto", "-h", target, "-C", "-p"),
                    _cmd("nikto", "-h", target, "-p"),
                    _cmd("nikto", "-h", target, "-d"),
                    _cmd("nikto", "-h", target, "-T"),
                ],
            },
        },
    },

    "wpscan": {
        "label": "WPSCAN",
        "ascii": r"""
        __          _______   _____  _____          _   _
        \ \        / /  __ \ / ____|/ ____|   /\   | \ | |
         \ \  /\  / /| |__) | (___ | |       /  \  |  \| |
          \ \/  \/ / |  ___/ \___ \| |      / /\ \ | . ` |
           \  /\  /  | |     ____) | |____ / ____ \| |\  |
            \/  \/   |_|    |_____/ \_____/_/    \_\_| \_|""",
        "modes": {
            "normal": {
                "label": "MODO NORMAL",
                "info": "Varredura padrão no WordPress.",
                "build": lambda target, **_: _cmd("wpscan", "--url", target),
            },
            "enumerate_users": {
                "label": "ENUMERAR USUÁRIOS",
                "info": "Enumera usuários registrados no WordPress.",
                "build": lambda target, **_: _cmd("wpscan", "--url", target, "--enumerate", "u"),
            },
            "enumerate_plugins": {
                "label": "ENUMERAR PLUGINS",
                "info": "Enumera plugins instalados e suas versões.",
                "build": lambda target, **_: _cmd("wpscan", "--url", target, "--enumerate", "p"),
            },
            "enumerate_themes": {
                "label": "ENUMERAR TEMAS",
                "info": "Enumera temas instalados e suas versões.",
                "build": lambda target, **_: _cmd("wpscan", "--url", target, "--enumerate", "t"),
            },
            "scan": {
                "label": "SCAN COMPLETO (API TOKEN)",
                "info": "Scan completo com verificação de vulnerabilidades via API.",
                "build": lambda target, api_token="", **_: _cmd(
                    "wpscan", "--url", target, "--api-token", api_token
                ),
            },
        },
    },
}


def build(tool: str, mode: str, target: str, **kwargs) -> list[str]:
    """Returns a single command as a list of args (safe for create_subprocess_exec)."""
    return REGISTRY[tool]["modes"][mode]["build"](target, **kwargs)


def build_multi(tool: str, mode: str, target: str, **kwargs) -> list[list[str]]:
    """Returns a list of commands for multi-step modes."""
    return REGISTRY[tool]["modes"][mode]["build"](target, **kwargs)


def is_multi(tool: str, mode: str) -> bool:
    return REGISTRY[tool]["modes"][mode].get("multi", False)


def info(tool: str, mode: str) -> str:
    return REGISTRY[tool]["modes"][mode].get("info", "")
