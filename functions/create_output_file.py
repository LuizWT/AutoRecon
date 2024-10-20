import os
from colorama import init, Fore

init(autoreset=True)

def create_output_file(script_name):
    output_dir = "output"

    output_file = os.path.join(output_dir, f"{script_name}_output.txt")
    os.makedirs(output_dir, exist_ok=True)
    return output_file

def execute_command_and_log(command, script_name):
    output_file = create_output_file(script_name)
    full_command = f"{command} >> {output_file} 2>&1"
    print(f"{Fore.YELLOW}Executando comando: {full_command}")
    os.system(full_command)
    print(f"{Fore.GREEN}Resultados salvos em: {output_file}")
