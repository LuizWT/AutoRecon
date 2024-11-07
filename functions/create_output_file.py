import os
from colorama import init, Fore
from functions.clear_terminal import clear_terminal
import asyncio

init(autoreset=True)

def create_output_file(script_name):
    output_dir = "output"
    output_file = os.path.join(output_dir, f"{script_name}_output.txt")
    os.makedirs(output_dir, exist_ok=True)
    return output_file

def execute_command_and_log(command, script_name):
    output_file = create_output_file(script_name)
    
    with open(output_file, 'a') as f:
        f.write(f"\n\n\nExecutando comando: {command}\n")
    
    print(f"{Fore.YELLOW}Executando comando: {command}")
    result = os.system(command + f" >> {output_file} 2>&1")

    clear_terminal()
    print(f"{Fore.GREEN}Resultados salvos em: {output_file}")


async def execute_command_and_log_submenu(command, tool_name):
    output_file = create_output_file(tool_name)
    
    with open(output_file, 'a') as f:
        f.write(f"\n\n\nExecutando comando: {command}\n")

    full_command = f"{command} >> {output_file} 2>&1"
    print(f"{Fore.YELLOW}Executando comando: {full_command}")

    process = await asyncio.create_subprocess_shell(
        full_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    with open(output_file, 'a') as f:
        if stdout:
            f.write(stdout.decode())
        if stderr:
            f.write(stderr.decode())

    clear_terminal()
    print(f"{Fore.GREEN}Resultados salvos em: {output_file}")
