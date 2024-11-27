<div align="center">
  <h1>AutoRecon</h1>
  <img src="https://github.com/user-attachments/assets/69dedab4-379b-4f19-9470-d5314cebdeec" alt="autorecon" width="200" height="200">
</div>

<hr>

### Descrição

O **AutoRecon** é um projeto de automação de ferramentas de segurança focado em facilitar o processo de varredura e coleta de informações em ambientes de rede. Ele integra diversas ferramentas de reconhecimento e varredura, como **Nmap**, **Sn1per**, **WPScan**, **Nuclei** e **Nikto**, oferecendo uma interface simplificada para realizar diversas operações com um único comando. O AutoRecon permite que administradores e profissionais de segurança testem e identifiquem vulnerabilidades em suas infraestruturas de maneira automatizada e organizada.

<hr>

### **Atualização 1.6.0**
Esta atualização introduz novas funcionalidades que aprimoram ainda mais a experiência do usuário e a flexibilidade do AutoRecon:

- **Otimização do Desempenho e Maior Estabilidade:**  
   A listagem e execução de comandos foram otimizadas, reduzindo a lentidão em filas extensas. Diversos bugs menores foram corrigidos, incluindo ajustes no gerenciamento de diretórios Git para garantir que os comandos sejam executados no local correto e a criação de funções para melhores validações, tornando o projeto mais robusto e confiável.

- **Verificação de Atualizações Inteligente:**  
   Agora o AutoRecon verifica o repositório antes de executar o comando `-update`, avisando o usuário nos casos que ocorrerem.

- **Melhorias no Menu de Scheduler:**  
   O menu de agendamento recebeu melhorias visuais (nova arte ASCII) e de usabilidade, diferenciando-se do menu principal e tornando a navegação mais intuitiva.
   Além disso, foi adicionado as seguintes opções e funcionalidades:
   
    - As ferramentas SNIPER e NUCLEI estão disponíveis no AR Scheduler.
   
    - Opção "[RA]" para remover todos os comandos da Queue.
   
    - Opção para usar ProxyChains: Entre em "[Q] Editar Queue" e utilize a opção "[P] Aplicar Proxychains" (a opção aparecerá apenas se houver um comando na lista), possibilitando adicionar o uso de ProxyChains para os comandos desejados. Veja o exemplo abaixo:

<div align="center">

![image](https://github.com/user-attachments/assets/077aaab5-e849-4110-9c58-e6afc71ee38b)

<hr>

![image](https://github.com/user-attachments/assets/5ac3ff7c-acec-410a-9715-e193c7c69c46)

</div>
  
- **Nova Funcionalidade de Lançadores:**  
A funcionalidade de **lançadores** no AutoRecon permite criar um atalho no menu do sistema para facilitar a execução da ferramenta com um ícone e comando pré-configurado. Para criar o lançador, basta executar o script `create_launcher.sh`:

Entre no diretório do projeto:

    ~$ cd ~/AutoRecon

Execute o script:

    ~$ bash launcher/create_launcher.sh

<hr>

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

> [!WARNING]  
> É altamente recomendado que a ferramenta seja instalada na pasta `home` (`~/AutoRecon`), pois isso garante a compatibilidade com o script de criação de lançadores e a configuração do alias "autorecon".

Clone o repositório:

    ~$ git clone https://github.com/LuizWT/AutoRecon.git ~/AutoRecon

Acesse o diretório:

    ~$ cd AutoRecon

Instale as dependências:

    ~$ sudo pip3 install -r requirements.txt

Execute a ferramenta:

    ~$ sudo python3 autorecon.py

Após a primeira execução, você terá a possibilidade de usar o alias "autorecon":

    ~$ sudo autorecon
  

### Atualização

Execute o comando:

    ~$ sudo autorecon -update

Caso o alias "autorecon" não esteja disponível:

    Entre no diretório do projeto AutoRecon:

        ~$ cd AutoRecon/

        ~$ sudo python3 autorecon.py -update

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
