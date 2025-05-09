from dataclasses import dataclass
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.validation import Validator, ValidationError
from functions.validations.is_valid import is_valid_ip_or_domain
from functions.clear_terminal import clear_terminal
from colorama import init, Fore
import asyncio

init(autoreset=True)

session = PromptSession()
bindings = KeyBindings()

@dataclass
class GlobalTarget:
    value: str | None = None

global_target = GlobalTarget()

class TargetValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(message="O alvo global não pode ser vazio.", cursor_position=0)
        if not is_valid_ip_or_domain(text):
            raise ValidationError(message="O alvo fornecido não é um IP ou domínio válido.", cursor_position=0)

async def set_global_target():
    clear_terminal()
    try:
        target = await session.prompt_async(
            HTML(f"<ansiyellow>Digite o alvo global (ex: 192.168.0.1 ou example.com):</ansiyellow> \n<ansiyellow>~$ </ansiyellow>"),
            validator=TargetValidator(),
            validate_while_typing=False,
            key_bindings=bindings
        )
        global_target.value = target.strip()
        clear_terminal()
        print(f"{Fore.YELLOW}[INFO] Alvo global definido: {Fore.GREEN}{global_target.value}\n{Fore.BLUE}Pressione Enter para continuar...")
        await session.prompt_async(HTML(""))
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {e}")
        print(f"{Fore.BLUE}Pressione Enter para retornar ao menu...")

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())
