from colorama import Fore, init

init(autoreset=True)

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        print(f"{Fore.YELLOW}Para o funcionamento da ferramenta, URL fornecido deve conter 'http://' ou 'https://'.\nEscolha qual protocolo será usado:\n{Fore.CYAN}[1] {Fore.RESET}https://\n{Fore.CYAN}[2] {Fore.RESET}http://")
        
        while True:
            choice = input(f"{Fore.GREEN}Escolha o protocolo do alvo [1/2]: ").strip()
            if choice == '1':
                return f"https://www.{url}"
            elif choice == '2':
                return f"http://www.{url}"
            else:
                print(f"{Fore.RED}Opção inválida. Por favor, escolha {Fore.GREEN}[1]{Fore.RED} para{Fore.GREEN} https://{Fore.RED} ou {Fore.GREEN}[2]{Fore.RED} para{Fore.GREEN} http://.")
    return url
