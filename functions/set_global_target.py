from dataclasses import dataclass
import os
import asyncio
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.document import Document
from functions.validations.is_valid import is_valid_ip_or_domain
from functions.clear_terminal import clear_terminal
from colorama import init, Fore

init(autoreset=True)

# Caminho fixo para o armazenamento do global target
BASE_DIR = Path(__file__).resolve().parent
QUEUE_DIR = BASE_DIR / "state"
QUEUE_FILE = QUEUE_DIR / "target.cfg"

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

# Cria o diretório e arquivo, se necessário
def ensure_queue_file():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    if not QUEUE_FILE.exists():
        QUEUE_FILE.write_text("")

# Lê a primeira linha do arquivo e, se válida, atribui a global_target.value. Caso contrário, limpa o arquivo.
def load_global_target():
    ensure_queue_file()
    lines = QUEUE_FILE.read_text().splitlines()
    if not lines:
        return
    first = lines[0].strip()
    if is_valid_ip_or_domain(first):
        global_target.value = first
    else:
        # Limpa todo o conteúdo se inválido
        QUEUE_FILE.write_text("")

# Salva a fila o global_target (sobrescreve)
def save_global_target(value: str):

    ensure_queue_file()
    QUEUE_FILE.write_text(value + os.linesep)

# Carrega valor de /state/target.cfg existente no início
load_global_target()

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

            # Validação manual após atribuir
            try:
                TargetValidator().validate(Document(text=target))
            except ValidationError as ve:
                print(f"{Fore.RED}[ERROR] {ve.message}")
                await asyncio.sleep(1)
                continue

            # Salvar somente após validação
            global_target.value = target
            save_global_target(target)

            # Confirmação com um único Enter
            clear_terminal()
            print(f"{Fore.YELLOW}[INFO] Alvo global definido: {Fore.GREEN}{global_target.value}")
            await session.prompt_async(
                HTML(f"<ansiblue>Pressione Enter (2x) para continuar...</ansiblue>"),
                validator=None,
                validate_while_typing=False
            )
            return

        except (KeyboardInterrupt, EOFError):
            clear_terminal()
            break
        except Exception as e:
            # Erro inesperado: única pausa
            clear_terminal()
            print(f"{Fore.RED}[ERROR] Erro inesperado: {e}")
            await session.prompt_async(
                HTML("<ansiblue>Pressione Enter para retornar ao menu...</ansiblue>"),
                validator=None,
                validate_while_typing=False
            )
            clear_terminal()
            return

@bindings.add('c-t')
def _(event):
    asyncio.create_task(set_global_target())
