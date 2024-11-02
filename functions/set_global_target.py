from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from functions.clear_terminal import clear_terminal
from colorama import init, Fore
import asyncio

init(autoreset=True)

session = PromptSession()
state = {
    "global_target": None
}

async def set_global_target():
    global state
    clear_terminal()
    
    try:
        state["global_target"] = await session.prompt_async(HTML(f"<ansigreen>Digite o alvo global (ex: 192.168.0.1 | site.com):</ansigreen> "))
        
        if not state["global_target"]:
            raise ValueError("O alvo global não pode ser vazio.")

        print(f"{Fore.YELLOW}Alvo global definido: {state['global_target']}\n{Fore.BLUE}Aperte Enter para continuar...")

    
    except Exception as e:
        print(f"{Fore.RED}Erro: {e}")
        await session.prompt_async(HTML(f"<ansiblue>Aperte Enter para tentar novamente...</ansiblue>"))


bindings = KeyBindings()

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())
