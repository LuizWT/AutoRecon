from dataclasses import dataclass
import os
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.document import Document
from functions.validations.is_valid import is_valid_ip_or_domain
from functions.clear_terminal import clear_terminal
from colorama import init, Fore

init(autoreset=True)

# Caminho para armazenar o alvo global
GLOBAL_TARGET_FILE = os.path.expanduser("~/.autorecon/global_target.txt")

session = PromptSession()
bindings = KeyBindings()

@dataclass
class GlobalTarget:
    value: str | None = None

global_target = GlobalTarget()

class TargetValidator(Validator):
    def validate(self, document: Document):
        text = document.text.strip()
        if not text:
            raise ValidationError(message="O alvo global não pode ser vazio.", cursor_position=0)
        if not is_valid_ip_or_domain(text):
            raise ValidationError(message="O alvo fornecido não é um IP ou domínio válido.", cursor_position=0)

async def set_global_target():
    while True:
        clear_terminal()
        try:
            raw = await session.prompt_async(
                HTML('<ansiyellow>Digite o alvo global (ex: 192.168.0.1 ou example.com):</ansiyellow>\n<ansiyellow>~$ </ansiyellow>'),
                validator=None,
                validate_while_typing=False,
                key_bindings=bindings
            )
            target = raw.strip()

            # Validação do target
            try:
                TargetValidator().validate(Document(text=target))
            except ValidationError as ve:
                print(f"{Fore.RED}[ERROR] {ve.message}")
                await session.prompt_async(
                    HTML("<ansiblue>Pressione Enter para tentar novamente...</ansiblue>"),
                    validator=None,
                    validate_while_typing=False
                )
                continue

            # Salvar apenas após a validação
            global_target.value = target
            os.makedirs(os.path.dirname(GLOBAL_TARGET_FILE), exist_ok=True)
            with open(GLOBAL_TARGET_FILE, 'w') as f:
                f.write(global_target.value)

            clear_terminal()
            await session.prompt_async(
                HTML(
                    f"<ansiyellow>[INFO] Alvo global definido: <ansigreen>{global_target.value}</ansigreen></ansiyellow>\n"
                    f"<ansiblue>Pressione Enter (2x) para continuar...</ansiblue>"
                ),
                validator=None,
                validate_while_typing=False
            )
            return

        except (KeyboardInterrupt, EOFError):
            clear_terminal()
            print(f"{Fore.RED}[INFO] Operação cancelada pelo usuário.\nPressione Enter para continuar...")
            return
        except Exception as e:
            # Corrige prompt único para erro inesperado
            print(f"{Fore.RED}[ERROR] Erro inesperado: {e}")
            await session.prompt_async(
                HTML("<ansiblue>Pressione Enter para retornar ao menu...</ansiblue>"),
                validator=None,
                validate_while_typing=False
            )
            return

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())
