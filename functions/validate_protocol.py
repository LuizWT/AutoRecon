from colorama import Fore, init
import re
init(autoreset=True)

# Função principal de validação da URL
def validate_url(url):

    if is_valid_url(url):
        return url
    
    # Remove o www. antes de validar a extensão do domínio
    url = validate_domain_extension(url)
    
    domain = url.split("://")[-1].split("/")[0]
    if domain.startswith("www."):
        domain = domain[4:]  # Remove o www.

    # Se o URL não começar com http:// ou https://, pede para o usuário escolher um protocolo
    if not url.startswith(('http://', 'https://')):
        print(f"{Fore.YELLOW}O URL não contém protocolo. Escolha qual protocolo será usado:\n{Fore.CYAN}[1] {Fore.RESET}https://\n{Fore.CYAN}[2] {Fore.RESET}http://")
        
        while True:
            choice = input(f"{Fore.GREEN}Escolha o protocolo do alvo [1/2]: ").strip()
            if choice == '1':
                url = f"https://www.{domain}"
                break
            elif choice == '2':
                url = f"http://www.{domain}"
                break
            else:
                print(f"{Fore.RED}Opção inválida. Por favor, escolha {Fore.GREEN}[1]{Fore.RED} para{Fore.GREEN} https://{Fore.RED} ou {Fore.GREEN}[2]{Fore.RED} para{Fore.GREEN} http://.")
    
    return url

# Função para validar a extensão do domínio
def validate_domain_extension(url):
    # Remoção do protocolo HTTP ou HTTPS para melhor funcionamento do REGEX
    domain = url.split("://")[-1].split("/")[0]
    
    # Se o domínio começar com www., remove
    if domain.startswith("www."):
        domain = domain[4:]

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

    # Retorna o domínio corrigido (sem o protocolo por enquanto)
    return f"{domain}"

def is_valid_url(url):
    # Verifica se a URL tem um protocolo e uma extensão de domínio válida
    pattern = r'^(https?://)?(www\.)?[\w-]+\.[a-z]{2,}(\.[a-z]{2,})*(/.*)?$'
    return bool(re.match(pattern, url))