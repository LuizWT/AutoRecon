import asyncio
import sys
from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

from functions.check_system import check_system
from functions.clear_terminal import clear_terminal
from functions.check_and_install_tool import check_and_install_tool
from functions.set_global_target import set_global_target, global_target
from functions.proxy_chains import ProxyManager
from functions.logger import get_logger
from configurations.ar_updater import parse_args, update_repository, new_version_checker
from configurations.configure_alias import configure_global_command
from configurations.version import __version__
from setup_tools.setup import TOOLS_CONFIG, install_tool
from tools.scheduler.automation_menu import automation_setup_menu
from tools.sniper import sniper_menu_loop
from tools.nmap import nmap_menu_loop
from tools.wpscan import wpscan_menu_loop
from tools.nuclei import nuclei_menu_loop
from tools.nikto import nikto_menu_loop
from config import OUTPUT_DIR

init(autoreset=True)
session = PromptSession()
logger = get_logger(__name__)

OUTPUT_DIR.mkdir(exist_ok=True)


def _main_menu() -> None:
    update_msg = (
        f"{Fore.RED}Desatualizado{Fore.YELLOW} - @LuizWt {Fore.RED}\n"
        f"    Use 'sudo autorecon --update' para atualizar"
        if new_version_checker()
        else f"{Fore.GREEN}Latest{Fore.YELLOW} - @LuizWt"
    )
    configure_global_command()

    proxychains_info = " (/etc/proxychains.conf)" if ProxyManager.check_installed() else ""
    proxychains_status = f"{Fore.GREEN}ON" if ProxyManager.is_enabled() else f"{Fore.RED}OFF"
    target_display = (
        f"Alvo: {Fore.GREEN}{global_target.value}{Fore.RESET}"
        if global_target.value
        else f"Alvo: {Fore.RED}Não definido{Fore.RESET}"
    )
    automation_status = f"{Fore.GREEN}ON" if global_target.value else f"{Fore.RED}OFF"

    print(rf"""
    {Fore.BLUE}{Style.BRIGHT}
                _        _____
     /\        | |      |  __ \      Pressione Ctrl+T para definir o alvo
    /  \  _   _| |_ ___ | |__) |___  ___ ___  _ __ {Fore.YELLOW}{target_display}{Fore.BLUE}{Style.BRIGHT}
   / /\ \| | | | __/ _ \|  _  // _ \/ __/ _ \| '_ \
  / ____ \ |_| | || (_) | | \ \  __/ (_| (_) | | | |
 /_/    \_\__,_|\__\___/|_|  \_\___|\___\___/|_| |_|

 {Fore.YELLOW}+ -- --=[ https://github.com/LuizWT/
 {Fore.YELLOW}+ -- --=[ AutoRecon {__version__} {update_msg}

    {Fore.CYAN}[1] {Fore.RESET}SNIPER
    {Fore.CYAN}[2] {Fore.RESET}NMAP
    {Fore.CYAN}[3] {Fore.RESET}WPSCAN
    {Fore.CYAN}[4] {Fore.RESET}NUCLEI
    {Fore.CYAN}[5] {Fore.RESET}NIKTO
    {Fore.CYAN}[0] {Fore.RESET}ProxyChains [{proxychains_status}{Fore.RESET}]{proxychains_info}
    {Fore.RED}[9] {Fore.RESET}Sair
    {Fore.YELLOW}[CTRL+A] {Fore.RESET}Automação [{automation_status}{Fore.RESET}]
    """)


async def main_loop() -> None:
    bindings = KeyBindings()

    @bindings.add("c-a")
    async def _(event):
        if global_target.value:
            clear_terminal()
            await automation_setup_menu()
        else:
            clear_terminal()
            logger.error(
                "Defina um alvo global antes de acessar a automação.\n"
                f"{Fore.CYAN}Pressione Enter para retornar..."
            )

    @bindings.add("c-t")
    def _(event):
        asyncio.create_task(set_global_target())

    OPTIONS = {
        "1": ("sniper", sniper_menu_loop),
        "2": ("nmap", nmap_menu_loop),
        "3": ("wpscan", wpscan_menu_loop),
        "4": ("nuclei", nuclei_menu_loop),
        "5": ("nikto", nikto_menu_loop),
    }

    while True:
        clear_terminal()
        _main_menu()

        option = await session.prompt_async(
            HTML("<ansiyellow>Escolha uma opção:</ansiyellow> "), key_bindings=bindings
        )
        option = option.strip()

        if option == "9":
            clear_terminal()
            logger.info("Saindo do AutoRecon.")
            break

        elif option in OPTIONS:
            tool_name, menu_func = OPTIONS[option]
            clear_terminal()
            await check_and_install_tool(tool_name, menu_func, global_target.value)

        elif option == "0":
            clear_terminal()
            if ProxyManager.check_installed():
                ProxyManager.toggle()
                status = "ativado" if ProxyManager.is_enabled() else "desativado"
                logger.info(f"ProxyChains {status}.")
            else:
                raw = await session.prompt_async(
                    HTML("<ansiyellow>ProxyChains não está instalado. Instalar? (y/n):</ansiyellow> ")
                )
                if raw.strip().lower() in ("y", "s"):
                    await install_tool("proxychains")
                    if ProxyManager.check_installed():
                        ProxyManager.toggle()
                    else:
                        logger.error("Falha ao instalar o ProxyChains.")
                await session.prompt_async(
                    HTML("<ansiyellow>Pressione Enter para retornar ao menu...</ansiyellow>")
                )


if __name__ == "__main__":
    if not check_system():
        sys.exit(1)

    args = parse_args()
    if args.update:
        update_repository()
        sys.exit(0)

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        clear_terminal()
        logger.info("Saindo do AutoRecon via Ctrl+C.")
