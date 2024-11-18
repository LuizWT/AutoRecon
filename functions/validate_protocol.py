from colorama import Fore, init
import re
init(autoreset=True)

def validate_url(url):
    # DEVE validar primeiramente a extensão do domínio
    url = validate_domain_extension(url)
    
    if not url.startswith(('http://www.', 'https://www.')):
        print(f"{Fore.YELLOW}Para o funcionamento da ferramenta, o URL fornecido deve conter 'http://www.' ou 'https://www.'.\nEscolha qual protocolo será usado:\n{Fore.CYAN}[1] {Fore.RESET}https://www.\n{Fore.CYAN}[2] {Fore.RESET}http://www.")
        
        while True:
            choice = input(f"{Fore.GREEN}Escolha o protocolo do alvo [1/2]: ").strip()
            if choice == '1':
                return f"https://www.{url}"
            elif choice == '2':
                return f"http://www.{url}"
            else:
                print(f"{Fore.RED}Opção inválida. Por favor, escolha {Fore.GREEN}[1]{Fore.RED} para{Fore.GREEN} https://{Fore.RED} ou {Fore.GREEN}[2]{Fore.RED} para{Fore.GREEN} http://.")
    
    return url

def validate_domain_extension(url):
    # Remoção do protocolo HTTP ou HTTPS para melhor funcionamento do REGEX
    domain = url.split("://")[-1].split("/")[0]

    if not re.search(r'\.\w{2,}(\.\w{2,})*$', domain):
        print(f"{Fore.YELLOW}O domínio fornecido não contém uma extensão válida.\n\nExemplos de extensões:\n{Fore.GREEN}.com, .org,\n.net, .br,\n.io, .edu")

        while True:
            extension = input(f"{Fore.YELLOW}Digite a extensão do domínio:{Fore.RESET} ").strip()

            # Verifica se a extensão está no formato correto, como: .com.br, .gov.sp, .org, etc.
            if re.match(r'^\.\w{2,}(\.\w{2,})*$', extension):
                domain += extension
                break
            else:
                print(f"{Fore.RED}A extensão fornecida é inválida. Tente novamente.")

    # URL com o domínio corrigido (sem protocolo por enquanto)
    return domain