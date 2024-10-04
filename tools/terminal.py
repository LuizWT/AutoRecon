import subprocess
import platform
import os


def open_terminal(command):
    os_type = platform.system()
    
    try:
        if os_type == 'Linux':
            # Tenta abrir um terminal compatível
            terminal_command = None
            
            try:
                terminal_command = ['gnome-terminal', '--', 'bash', '-c', f"{command}; read -p 'Pressione Enter para fechar..'"]
                subprocess.run(terminal_command, check=True)
            except FileNotFoundError:
                try:
                    terminal_command = ['konsole', '-e', 'bash', '-c', f"{command}; read -p 'Pressione Enter para fechar..'"]
                    subprocess.run(terminal_command, check=True)
                except FileNotFoundError:
                    try:
                        terminal_command = ['xfce4-terminal', '--', 'bash', '-c', f"{command}; read -p 'Pressione Enter para fechar..'"]
                        subprocess.run(terminal_command, check=True)
                    except FileNotFoundError:
                        try:
                            terminal_command = ['xterm', '-e', f"{command}; read -p 'Pressione Enter para fechar..'"]
                            subprocess.run(terminal_command, check=True)
                        except FileNotFoundError:
                            print("Nenhum terminal disponível encontrado.") 
        else:
            print("Sistema operacional não suportado.")
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao abrir o terminal: {e}")
