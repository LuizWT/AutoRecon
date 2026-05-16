import asyncio
from colorama import Fore, init
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

from functions.clear_terminal import clear_terminal
from functions.logger import get_logger
from functions.set_global_target import global_target, set_global_target
from functions.toggle_info import toggle_info, is_info_visible
from functions.validations.validate_ports import validate_ports
import tools.registry as registry
from tools.common import dispatch

init(autoreset=True)
session = PromptSession()
logger = get_logger(__name__)

_bindings = KeyBindings()


@_bindings.add("c-t")
def _(event):
    asyncio.create_task(set_global_target())


async def _get_scan_technique() -> str | None:
    clear_terminal()
    print(f"""
    {Fore.CYAN}[1]{Fore.RESET} -sS  TCP SYN Scan
    {Fore.CYAN}[2]{Fore.RESET} -sT  TCP Connect Scan
    {Fore.CYAN}[3]{Fore.RESET} -sU  UDP Scan
    {Fore.CYAN}[4]{Fore.RESET} -sF  TCP FIN Scan
    {Fore.CYAN}[5]{Fore.RESET} -sN  TCP NULL Scan
    {Fore.CYAN}[6]{Fore.RESET} -sX  TCP Xmas Scan
    {Fore.CYAN}[7]{Fore.RESET} Todas as técnicas
    """)
    choice = await session.prompt_async(
        HTML("<ansigreen>Técnica</ansigreen> <ansired>[B voltar]</ansired><ansigreen>:</ansigreen> ")
    )
    mapping = {
        "1": "-sS", "2": "-sT", "3": "-sU",
        "4": "-sF", "5": "-sN", "6": "-sX", "7": "all",
    }
    if choice.lower() == "b":
        return None
    result = mapping.get(choice.strip())
    if result is None:
        logger.error("Opção inválida.")
        return await _get_scan_technique()
    return result


async def _get_ports() -> str | None:
    while True:
        raw = await session.prompt_async(
            HTML(
                "<ansigreen>Portas (ex: 21,22 ou 1-100)</ansigreen>"
                " <ansired>[B voltar]</ansired><ansigreen>:</ansigreen> "
            )
        )
        if raw.strip().lower() == "b":
            return None
        if validate_ports(raw.strip()):
            return raw.strip()
        logger.error("Formato inválido. Use: 21,22 ou 1-100.")


async def _get_timing() -> str | None:
    while True:
        raw = await session.prompt_async(
            HTML(
                "<ansigreen>Nível de timing (0-5)</ansigreen>"
                " <ansired>[B voltar]</ansired><ansigreen>:</ansigreen> "
            )
        )
        if raw.strip().lower() == "b":
            return None
        v = raw.strip()
        if v.isdigit() and 0 <= int(v) <= 5:
            return v
        logger.error("Nível inválido. Use 0 a 5.")


def _info(mode: str) -> str:
    if not is_info_visible():
        return ""
    return f"  {Fore.CYAN}|{Fore.BLUE} {registry.info('nmap', mode)}{Fore.RESET}"


async def nmap_menu_loop(action: str = "run") -> None:
    mode_label = "Automação" if action == "queue" else "Execução"
    m = registry.REGISTRY["nmap"]["modes"]

    while True:
        clear_terminal()
        target = global_target.value
        target_display = (
            f"{Fore.GREEN}{target}{Fore.RESET}" if target
            else f"{Fore.RED}Não definido{Fore.RESET}"
        )

        print(rf"""
        {Fore.BLUE}
        _ __  _ __ ___   __ _ _ __    Ctrl+T → definir alvo
        | '_ \| '_ ` _ \ / _` | '_ \  Alvo: {target_display}{Fore.BLUE}
        | | | | | | | | | (_| | |_) |  Modo: {Fore.YELLOW}{mode_label}{Fore.BLUE}
        |_| |_|_| |_| |_|\__,_| .__/
                              | |
                              |_|
        {Fore.CYAN}[1] {Fore.RESET}{m['target_spec']['label']}{_info('target_spec')}
        {Fore.CYAN}[2] {Fore.RESET}{m['scan_technique']['label']}{_info('scan_technique')}
        {Fore.CYAN}[3] {Fore.RESET}{m['host_discovery']['label']}{_info('host_discovery')}
        {Fore.CYAN}[4] {Fore.RESET}{m['port_spec']['label']}{_info('port_spec')}
        {Fore.CYAN}[5] {Fore.RESET}{m['service_detection']['label']}{_info('service_detection')}
        {Fore.CYAN}[6] {Fore.RESET}{m['os_detection']['label']}{_info('os_detection')}
        {Fore.CYAN}[7] {Fore.RESET}{m['timing']['label']}{_info('timing')}
        {Fore.CYAN}[8] {Fore.RESET}{m['http_title']['label']}{_info('http_title')}
        {Fore.CYAN}[9] {Fore.RESET}{m['ssl_cert']['label']}{_info('ssl_cert')}
        {Fore.CYAN}[10]{Fore.RESET} {m['vuln']['label']}{_info('vuln')}
        {Fore.CYAN}[11]{Fore.RESET} {m['smb_os_discovery']['label']}{_info('smb_os_discovery')}
        {Fore.CYAN}[12]{Fore.RESET} {m['http_robots_txt']['label']}{_info('http_robots_txt')}
        {Fore.CYAN}[13]{Fore.RESET} {m['ssh_hostkey']['label']}{_info('ssh_hostkey')}
        {Fore.CYAN}[14]{Fore.RESET} {m['dns_brute']['label']}{_info('dns_brute')}
        {Fore.CYAN}[15]{Fore.RESET} {m['all_commands']['label']}{_info('all_commands')}
        {Fore.RED}[B] {Fore.RESET}Voltar   {Fore.YELLOW}[I]{Fore.RESET} Alternar Informações
        """)

        option = await session.prompt_async(
            HTML("<ansiyellow>Escolha:</ansiyellow> "), key_bindings=_bindings
        )
        option = option.strip()

        if option.lower() == "b":
            break
        if option.lower() == "i":
            toggle_info()
            continue

        target = global_target.value
        if not target:
            logger.error("Nenhum alvo definido. Pressione Ctrl+T para configurar.")
            await session.prompt_async(HTML("<ansiblue>Enter para continuar...</ansiblue>"))
            continue

        if option == "1":
            await dispatch(action, "nmap", "target_spec",
                           [registry.build("nmap", "target_spec", target)])

        elif option == "2":
            technique = await _get_scan_technique()
            if technique is None:
                continue
            if technique == "all":
                cmds = [
                    registry.build("nmap", "scan_technique", target, technique=t)
                    for t in ("-sS", "-sT", "-sU", "-sF", "-sN", "-sX")
                ]
            else:
                cmds = [registry.build("nmap", "scan_technique", target, technique=technique)]
            await dispatch(action, "nmap", "scan_technique", cmds)

        elif option == "3":
            await dispatch(action, "nmap", "host_discovery",
                           [registry.build("nmap", "host_discovery", target)])

        elif option == "4":
            ports = await _get_ports()
            if ports is None:
                continue
            await dispatch(action, "nmap", "port_spec",
                           [registry.build("nmap", "port_spec", target, ports=ports)])

        elif option == "5":
            await dispatch(action, "nmap", "service_detection",
                           [registry.build("nmap", "service_detection", target)])

        elif option == "6":
            await dispatch(action, "nmap", "os_detection",
                           [registry.build("nmap", "os_detection", target)])

        elif option == "7":
            level = await _get_timing()
            if level is None:
                continue
            await dispatch(action, "nmap", "timing",
                           [registry.build("nmap", "timing", target, level=level)])

        elif option == "8":
            await dispatch(action, "nmap", "http_title",
                           [registry.build("nmap", "http_title", target)])

        elif option == "9":
            await dispatch(action, "nmap", "ssl_cert",
                           [registry.build("nmap", "ssl_cert", target)])

        elif option == "10":
            await dispatch(action, "nmap", "vuln",
                           [registry.build("nmap", "vuln", target)])

        elif option == "11":
            await dispatch(action, "nmap", "smb_os_discovery",
                           [registry.build("nmap", "smb_os_discovery", target)])

        elif option == "12":
            await dispatch(action, "nmap", "http_robots_txt",
                           [registry.build("nmap", "http_robots_txt", target)])

        elif option == "13":
            await dispatch(action, "nmap", "ssh_hostkey",
                           [registry.build("nmap", "ssh_hostkey", target)])

        elif option == "14":
            await dispatch(action, "nmap", "dns_brute",
                           [registry.build("nmap", "dns_brute", target)])

        elif option == "15":
            if action == "run":
                confirm = await session.prompt_async(
                    HTML(
                        "<ansired>Executar 16 comandos em sequência? Pode levar horas."
                        " (y/n):</ansired> "
                    )
                )
                if confirm.strip().lower() not in ("y", "s"):
                    continue
            await dispatch(action, "nmap", "all_commands",
                           registry.build_multi("nmap", "all_commands", target))
