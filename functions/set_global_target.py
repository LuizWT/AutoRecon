from functions.validations.is_valid import is_valid_ip_or_domain
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
        while True:
            target = await session.prompt_async(HTML(f"<ansiyellow>Digite o alvo global\nExemplos:</ansiyellow> <ansigreen>192.168.0.1</ansigreen> <ansiyellow>ou</ansiyellow> <ansigreen>example.com</ansigreen>\n\n<ansiyellow>~$</ansiyellow> "))
            
            if not target.strip():
                clear_terminal()
                print(f"{Fore.RED}[ERROR] O alvo global não pode ser vazio. Tente novamente.\n")
                continue

            if not is_valid_ip_or_domain(target):
                clear_terminal()
                print(f"{Fore.RED}[ERROR] O alvo fornecido não é um IP ou domínio válido.")
                continue
                
            state["global_target"] = target
            clear_terminal()
            print(f"{Fore.YELLOW}[INFO] Alvo global definido: {Fore.GREEN}{state['global_target']}\n{Fore.BLUE}Aperte Enter para continuar...")
            break
    
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {e}")
        print(rf"{Fore.BLUE}Aperte Enter para voltar ao menu...")

bindings = KeyBindings()

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())
