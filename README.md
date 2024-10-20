# AutoRecon

### Descrição

O **AutoRecon** é um projeto de automação de ferramentas de segurança focado em facilitar o processo de varredura e coleta de informações em ambientes de rede. Ele integra diversas ferramentas de reconhecimento e varredura, como **Nmap** e **Sn1per**, oferecendo uma interface simplificada para realizar diversas operações com um único comando. O AutoRecon permite que administradores e profissionais de segurança testem e identifiquem vulnerabilidades em suas infraestruturas de maneira automatizada e organizada.

### Funcionalidades

- **Automatização de Nmap**: Execute varreduras do Nmap automaticamente com diferentes modos e técnicas, como detecção de serviços, descoberta de hosts, verificação de vulnerabilidades e força bruta de DNS.
- **Execução Sequencial**: Execute múltiplos comandos em sequência para uma varredura completa, evitando a necessidade de rodar cada comando individualmente.
- **Instalação Automática**: O AutoRecon verifica e instala automaticamente ferramentas essenciais, como Nmap e Sn1per. O usuário não é obrigado a instalar todas as ferramentas de terceiros, mas apenas as que pretende usar, sendo perguntado antes da instalação.
- **Execução de Ferramentas de Terceiros**: Integração com **Sn1per**, uma ferramenta de reconhecimento de rede, para realizar operações de inteligência de código aberto (OSINT) e varredura de vulnerabilidades.
- **Opção de Uso de Proxychains**: Execute varreduras através do **proxychains**, adicionando uma camada de anonimato durante os testes de segurança.
- **Relatório de Resultados**: Salve automaticamente os resultados das varreduras em arquivos para análise posterior.

### Compatibilidade

Atualmente, o AutoRecon é compatível apenas com sistemas operacionais baseados em **Linux**.

### Ferramentas Suportadas

- **Nmap** (inclui diversas técnicas de varredura TCP, UDP, descoberta de hosts, entre outros)
- **Sn1per** (para reconhecimento de rede e OSINT)

### Instalação

Clone o repositório:

    ~$ git clone https://github.com/seu-usuario/AutoRecon.git

Acesse o diretório:

    ~$ cd AutoRecon

Execute a ferramenta:

    ~$ python3 main.py

### Uso

O AutoRecon possui um menu interativo que facilita a execução de diferentes modos de varredura.
No menu, você pode escolher diferentes tipos de varredura, como:
    
- Especificação de Alvo
- Técnicas de Varredura (TCP, UDP, ACK, etc.)
- Descoberta de Hosts
- Detecção de Sistema Operacional
- Execução de todos os comandos em sequência

### Contribuições

Se você quiser contribuir com o projeto, sinta-se à vontade para abrir issues ou fazer pull requests no repositório oficial do projeto.
_________________________________________________________________
## Apoio ao Projeto

Se você gostaria de apoiar o projeto, considere fazer uma doação:

**BTC Wallet**:  
`bc1qfy534ujs9yekwthe063fck0zf7hel7paem6sxl`

_________________________________________________________________
Este projeto está licenciado sob a MIT License.
