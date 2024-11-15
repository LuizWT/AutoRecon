# AutoRecon

### Descrição

O **AutoRecon** é um projeto de automação de ferramentas de segurança focado em facilitar o processo de varredura e coleta de informações em ambientes de rede. Ele integra diversas ferramentas de reconhecimento e varredura, como **Nmap**, **Sn1per**, **WPScan**, **Nuclei** e **Nikto**, oferecendo uma interface simplificada para realizar diversas operações com um único comando. O AutoRecon permite que administradores e profissionais de segurança testem e identifiquem vulnerabilidades em suas infraestruturas de maneira automatizada e organizada.

### Funcionalidades
- **Automatização de Ferramentas**: Execute varreduras do Nmap, Nuclei, WPScan, Nikto e outras ferramentas, com diferentes modos e técnicas como detecção de serviços, descoberta de hosts, verificação de vulnerabilidades e força bruta de DNS.
- **Execução Sequencial**: Execute múltiplos comandos em sequência para uma varredura completa, evitando a necessidade de rodar cada comando individualmente.
- **Instalação Automática**: O AutoRecon verifica e instala automaticamente ferramentas essenciais, como Nmap, Sn1per, WPScan, Nuclei e Nikto. O usuário não é obrigado a instalar todas as ferramentas de terceiros, mas apenas as que pretende usar, sendo perguntado antes da instalação.
- **Execução de Ferramentas de Terceiros**: Integração com **Sn1per** para reconhecimento de rede, **WPScan** para varredura de vulnerabilidades de WordPress, **Nuclei** para execução de scans de segurança baseados em templates, **Nikto** para verificar vulnerabilidades em servidores web e **Nmap** para escaneamento e descoberta de rede.
- **Opção de Uso de Proxychains**: Execute varreduras através do **proxychains**, adicionando uma camada de anonimato durante os testes de segurança.
- **Relatório de Resultados**: É salvo automaticamente os resultados das varreduras em arquivos para análise posterior em `output/`.
  
<hr>

### AR SCHEDULER
- **Submenu de Automação**: Adicione comandos a uma fila (queue) personalizada e configure um intervalo de execução para cada um.
- **Comandos Customizados**: É possível criar e executar comandos específicos diretamente, sem as limitações dos predefinidos.
- **Edição da Fila de Execução**: Visualize, edite ou remova comandos da fila para adaptar o escopo das execuções conforme necessário.
- **Intervalo de Execução Personalizável**: Defina intervalos customizados para a execução automática de comandos, tornando o processo mais adaptável às necessidades de cada análise.
  
<hr>

### Atualizações v1.3.0
Esta atualização introduz novas funcionalidades que aprimoram a experiência do usuário e tornam o AutoRecon mais eficiente e flexível. As principais mudanças incluem:

- **Criação do Alias Global `autorecon`:** O AutoRecon agora é como um comando global no sistema, permitindo que seja executado de qualquer lugar utilizando o comando `sudo autorecon`. Isso facilita o acesso e a execução do script, sem a necessidade de navegar até o diretório específico.

- **Adição do comando `-update`:** Agora é possível atualizar o código do AutoRecon diretamente pela linha de comando, garantindo que os usuários sempre utilizem a versão mais recente do projeto. Este comando automatiza o processo de *git pull* e *git fetch* para manter o repositório sincronizado com a última versão bastanto escrever **`sudo autorecon -update`**.
  
<hr>
  
### Compatibilidade

Atualmente, o AutoRecon é compatível apenas com sistemas operacionais baseados em **Linux**.
  
<hr>

### Ferramentas Suportadas

- **Nmap** (Técnicas de varredura TCP, UDP, descoberta de hosts, entre outros)
- **Sn1per** (Reconhecimento de rede e OSINT)
- **WPScan** (Varredura e análise de vulnerabilidades de sites WordPress)
- **Nuclei** (Execução de scans de segurança com base em templates personalizáveis)
- **Nikto** (Verificação de vulnerabilidades em servidores web)
  
<hr>

### Instalação

Clone o repositório:

    ~$ git clone https://github.com/LuizWT/AutoRecon.git

Acesse o diretório:

    ~$ cd AutoRecon

Instale as dependências:

    ~$ sudo pip install -r requirements.txt

Execute a ferramenta:

    ~$ sudo python3 autorecon.py
  
<hr>

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
  
<hr>

## Apoio ao Projeto

Se você quiser contribuir com o projeto, sinta-se à vontade para abrir Issues ou fazer Pull Requests no repositório oficial do projeto.
  
Quer apoiar ainda mais? Faça uma doação e ajude a manter este projeto vivo!

**BTC Wallet**:  
`bc1qfy534ujs9yekwthe063fck0zf7hel7paem6sxl`
  
<hr>

Este projeto está licenciado sob a MIT License.
