import subprocess
from colorama import Fore, init
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

from functions.clear_terminal import clear_terminal
from functions.logger import get_logger
from setup_tools.setup import TOOLS_CONFIG, install_tool

init(autoreset=True)
session = PromptSession()
logger = get_logger(__name__)


def _check_installed(tool_name: str) -> bool:
    config = TOOLS_CONFIG.get(tool_name)
    if not config:
        return False
    try:
        result = subprocess.run(
            config["check_command"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if "min_version" in config:
            version_output = result.stdout.decode().split()[1]
            return version_output >= config["min_version"]
        return result.returncode == 0
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError):
        return False


async def _ask_install(prompt_text: str) -> bool:
    answer = await session.prompt_async(HTML(f"<ansiyellow>{prompt_text}</ansiyellow>"))
    return answer.strip().lower() in ("y", "s")


async def check_and_install_tool(tool_name: str, menu_func, global_target: str) -> None:
    config = TOOLS_CONFIG.get(tool_name)
    if not config:
        logger.error(f"Configuração para '{tool_name}' não encontrada.")
        return

    logger.info(f"Verificando instalação de {tool_name}...")
    install_cmds = config.get("install_commands", {})

    if install_cmds.get("ruby_required") and not _check_installed("ruby"):
        if not await _ask_install(f"{tool_name} requer Ruby. Instalar Ruby e {tool_name}? (y/n): "):
            logger.info("Retornando ao menu principal.")
            return
        await install_tool("ruby")
        await install_tool(tool_name)
        logger.info(f"Abrindo menu {tool_name.upper()}...")
        await menu_func()
        return

    if install_cmds.get("go_required") and not _check_installed("go"):
        if not await _ask_install(f"{tool_name} requer Go. Instalar Go e {tool_name}? (y/n): "):
            logger.info("Retornando ao menu principal.")
            return
        await install_tool("go")
        await install_tool(tool_name)
        logger.info(f"Abrindo menu {tool_name.upper()}...")
        await menu_func()
        return

    if _check_installed(tool_name):
        logger.info(f"Abrindo menu {tool_name.upper()}...")
        await menu_func()
        return

    if not await _ask_install(f"{tool_name} não está instalado. Instalar? (y/n): "):
        logger.info("Retornando ao menu principal.")
        return

    await install_tool(tool_name)
    if _check_installed(tool_name):
        logger.info(f"Abrindo menu {tool_name.upper()}...")
        await menu_func()
    else:
        logger.error(f"Falha ao instalar {tool_name}. Verifique a saída acima.")
