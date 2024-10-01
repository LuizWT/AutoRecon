# AutoRecon

### Descrição

O AutoRecon é um projeto de automatização de ferramentas de segurança focado em facilitar o processo de varredura e coleta de informações em ambientes de rede. Ele integra diversas ferramentas de reconhecimento e varredura, como Nmap e Sn1per, oferecendo uma interface simplificada para realizar diversas operações com um único comando. O AutoRecon permite que administradores e profissionais de segurança testem e identifiquem vulnerabilidades em suas infraestruturas de maneira automatizada e organizada.
Funcionalidades

    Automatização de Nmap: O AutoRecon permite executar varreduras do Nmap automaticamente com diferentes modos e técnicas, como detecção de serviços, descoberta de hosts, verificação de vulnerabilidades e força bruta de DNS.
    Execução Sequencial: Você pode executar múltiplos comandos em sequência para varredura completa, evitando a necessidade de rodar cada comando individualmente.
    Instalação Automática: Verifica e instala automaticamente ferramentas essenciais, como Nmap e Sn1per, garantindo que o ambiente esteja pronto para ser utilizado.
    Execução de Ferramentas de Terceiros: Integração com Sn1per, uma ferramenta de reconhecimento de rede, para realizar operações de inteligência de código aberto (OSINT) e varredura de vulnerabilidades.
    Relatório de Resultados: Os resultados das varreduras podem ser salvos automaticamente em arquivos para análise posterior.

### Compatibilidade

Atualmente, o AutoRecon é compatível apenas com sistemas operacionais baseados em Linux, suportando as seguintes distribuições:

    Debian/Ubuntu: Instalando pacotes via apt-get.
    Red Hat/Fedora/CentOS: Utilizando dnf para instalação.
    openSUSE: Instalando pacotes via zypper.

### Ferramentas Suportadas:

    Nmap (inclui diversas técnicas de varredura TCP, UDP, descoberta de hosts, entre outros)
    Sn1per (para reconhecimento de rede e OSINT)

### Instalação

    Clone o repositório do AutoRecon:

```~$ git clone https://github.com/seu-usuario/AutoRecon.git```

```~$ cd AutoRecon```

```~$ python3 setup_tools.py```

Uso

O AutoRecon possui um menu interativo que facilita a execução de diferentes modos de varredura.
No menu, você pode escolher diferentes tipos de varredura, como:

    Especificação de Alvo
    Técnicas de Varredura (TCP, UDP, ACK, etc.)
    Descoberta de Hosts
    Detecção de Sistema Operacional
    Execução de todos os comandos em sequência

Exemplos de Uso

    Varredura Simples: Escolha a opção "Especificação de Alvo" para realizar uma varredura simples em um endereço IP ou domínio.

    Execução Sequencial de Comandos: Utilize a opção "Executar Todos os Comandos" para aplicar várias técnicas de varredura de uma vez, bastando fornecer o alvo.

Contribuições

Se você quiser contribuir com o projeto, sinta-se à vontade para abrir issues ou fazer pull requests no repositório oficial do projeto.
Licença

BTC wallet: bc1qfy534ujs9yekwthe063fck0zf7hel7paem6sxl

Este projeto está licenciado sob a MIT License.
