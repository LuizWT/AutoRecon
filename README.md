# AutoRecon

### Descrição

O **AutoRecon** é um projeto de automação de ferramentas de segurança focado em facilitar o processo de varredura e coleta de informações em ambientes de rede. Ele integra diversas ferramentas de reconhecimento e varredura, como **Nmap**, **Sn1per**, **WPScan**, **Nuclei** e **Nikto**, oferecendo uma interface simplificada para realizar diversas operações com um único comando. O AutoRecon permite que administradores e profissionais de segurança testem e identifiquem vulnerabilidades em suas infraestruturas de maneira automatizada e organizada.

### Funcionalidades

- **Automatização de Ferramentas**: Execute varreduras do Nmap, Nuclei, WPScan, Nikto, e outras ferramentas, com diferentes modos e técnicas, como detecção de serviços, descoberta de hosts, verificação de vulnerabilidades e força bruta de DNS.
- **Execução Sequencial**: Execute múltiplos comandos em sequência para uma varredura completa, evitando a necessidade de rodar cada comando individualmente.
- **Instalação Automática**: O AutoRecon verifica e instala automaticamente ferramentas essenciais, como Nmap, Sn1per, WPScan, Nuclei e Nikto. O usuário não é obrigado a instalar todas as ferramentas de terceiros, mas apenas as que pretende usar, sendo perguntado antes da instalação.
- **Execução de Ferramentas de Terceiros**: Integração com **Sn1per** para reconhecimento de rede, **WPScan** para varredura de vulnerabilidades de WordPress, **Nuclei** para execução de scans de segurança baseados em templates e **Nikto** para verificar vulnerabilidades em servidores web.
- **Opção de Uso de Proxychains**: Execute varreduras através do **proxychains**, adicionando uma camada de anonimato durante os testes de segurança.
- **Relatório de Resultados**: Salve automaticamente os resultados das varreduras em arquivos para análise posterior.

### Compatibilidade

Atualmente, o AutoRecon é compatível apenas com sistemas operacionais baseados em **Linux**.

### Ferramentas Suportadas

- **Nmap** (Técnicas de varredura TCP, UDP, descoberta de hosts, entre outros)
- **Sn1per** (Reconhecimento de rede e OSINT)
- **WPScan** (Varredura e análise de vulnerabilidades de sites WordPress)
- **Nuclei** (Execução de scans de segurança com base em templates personalizáveis)
- **Nikto** (Verificação de vulnerabilidades em servidores web)

### Instalação

Clone o repositório:

    ~$ git clone https://github.com/seu-usuario/AutoRecon.git

Acesse o diretório:

    ~$ cd AutoRecon

Instale as dependências:

    ~$ sudo pip install -r requirements.txt

Execute a ferramenta:

    ~$ sudo python3 autorecon.py

### Uso

O AutoRecon possui um menu interativo que facilita a execução de diferentes modos de varredura a partir de outras ferramentas. Ao decorrer dos menus que forem sendo escolhidos, você se deparará com várias opções, incluindo:

- **Especificação de Alvo**: Informe o endereço IP ou domínio que deseja analisar.
- **Técnicas de Varredura**: Selecione entre varreduras TCP, UDP, ACK, entre outras.
- **Descoberta de Hosts**: Identifique hosts ativos na rede.
- **Detecção de Sistema Operacional**: Detecte o sistema operacional dos dispositivos alvo.
- **Varredura de Vulnerabilidades em WordPress com WPScan**: Realize uma análise de segurança focada em sites WordPress.
- **Execução de Scans com Nuclei**: Utilize templates para verificar vulnerabilidades específicas em aplicações.
- **Verificação de Vulnerabilidades com Nikto**: Analise servidores web em busca de configurações inseguras e vulnerabilidades conhecidas.
- **Execução de Todos os Comandos em Sequência**: Execute uma sequência completa de scans para uma análise abrangente.

### Contribuições

Se você quiser contribuir com o projeto, sinta-se à vontade para abrir issues ou fazer pull requests no repositório oficial do projeto.
_________________________________________________________________
## Apoio ao Projeto

Se você gostaria de apoiar o projeto, considere fazer uma doação:

**BTC Wallet**:  
`bc1qfy534ujs9yekwthe063fck0zf7hel7paem6sxl`

_________________________________________________________________
Este projeto está licenciado sob a MIT License.
