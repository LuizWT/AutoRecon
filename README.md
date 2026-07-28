<div align="center">
  <h1>AutoRecon</h1>
<hr>

### Descrição

O **AutoRecon** é um projeto de automação de ferramentas de segurança focado em facilitar o processo de varredura e coleta de informações em ambientes de rede. Ele integra diversas ferramentas de reconhecimento e varredura, como **Nmap**, **Sn1per**, **WPScan**, **Nuclei** e **Nikto**, oferecendo uma interface simplificada para realizar diversas operações com um único comando. O AutoRecon permite que administradores e profissionais de segurança testem e identifiquem vulnerabilidades em suas infraestruturas de maneira automatizada e organizada.

<hr>

### **Atualização 1.8.0**

Esta versão introduz o **`autorecon scan`** — varredura orquestrada multi-ferramenta via perfis YAML — e refatora as definições de comandos para um formato declarativo.

- **Varredura por Perfis (`autorecon scan`)**  
  Execute múltiplas ferramentas em sequência com um único comando, informando apenas o alvo e o perfil desejado. O resultado é salvo automaticamente como relatório Markdown em `output/`.

- **Perfis Prontos**  
  Três perfis incluídos: `web-app`, `network-recon` e `full-recon`. Liste-os com `autorecon profiles`.

- **Relatório Markdown Automático**  
  Após cada varredura, um relatório estruturado é gerado em `output/` com status de cada etapa, saída completa das ferramentas e tempo de execução.

- **Definições de Ferramentas em YAML**  
  Os comandos de cada ferramenta (nmap, nikto, nuclei, wpscan, sniper) foram migrados para arquivos YAML em `tools/definitions/`. Adicionar ou ajustar um modo não requer mais editar código Python.


<hr>

### Funcionalidades
- **Varredura por Perfis**: Execute múltiplas ferramentas em sequência com `autorecon scan --target X --profile Y`. Perfis são arquivos YAML que definem quais ferramentas e modos rodar em ordem.
- **Relatório Markdown Automático**: Após cada varredura via `scan`, um relatório estruturado é salvo em `output/` com status, saída e tempo de execução de cada etapa.
- **Perfis Personalizáveis**: Crie seus próprios perfis em `profiles/` combinando qualquer ferramenta e modo disponível.
- **Menu Interativo (TUI)**: Interface de terminal para execução manual e exploração individual de cada ferramenta.
- **Automatização com Fila (AR Scheduler)**: Adicione comandos a uma fila e execute-os com intervalo configurável.
- **Instalação Automática**: Verifica e instala ferramentas sob demanda — apenas quando o usuário decide utilizá-las.
- **Suporte a ProxyChains**: Execute varreduras através do proxychains para anonimato adicional.
- **Definições em YAML**: Modos de cada ferramenta são declarados em `tools/definitions/`, facilitando adição e manutenção sem alterar código Python.
  
<hr>

### AR SCHEDULER
- **Submenu de Automação**: Adicione comandos a uma fila (queue) personalizada e configure um intervalo de execução para cada um.
- **Comandos Customizados**: É possível criar e executar comandos específicos diretamente, sem as limitações dos predefinidos.
- **Edição da Fila de Execução**: Visualize, edite ou remova comandos da fila para adaptar o escopo das execuções conforme necessário.
- **Intervalo de Execução Personalizável**: Defina intervalos customizados para a execução automática de comandos, tornando o processo mais adaptável às necessidades de cada análise.
  
<hr>
  
### Compatibilidade

Atualmente, o AutoRecon é compatível apenas com sistemas operacionais baseados em **Linux**.
> [!WARNING]  
> A ferramenta apenas foi testada nas seguintes distros:
> Debian, Fedora, OpenSUSE e Arch Linux.
  
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
> Para isso, utilize o comando abaixo para realizar a instalação.


    bash <(curl -sSL https://raw.githubusercontent.com/LuizWT/AutoRecon/main/configurations/autorecon.sh)
  

### Atualização

Execute o comando:

    sudo autorecon -u
ou

    sudo autorecon --update 

<hr>

### Uso

#### Menu interativo (TUI)

Execute sem argumentos para abrir o menu interativo:

    sudo autorecon

No menu você escolhe a ferramenta, o modo de varredura e define o alvo. As opções disponíveis incluem:

- **Especificação de Alvo** — IP, domínio ou CIDR.
- **Técnicas de Varredura** — TCP, UDP, ACK, FIN, NULL, Xmas e outras.
- **Descoberta de Hosts** — identifica hosts ativos na rede.
- **Detecção de Sistema Operacional** — SO do dispositivo alvo.
- **WPScan** — varredura de vulnerabilidades em WordPress.
- **Nuclei** — scans baseados em templates personalizáveis.
- **Nikto** — verificação de vulnerabilidades em servidores web.
- **Execução em Sequência** — todos os comandos de uma ferramenta de uma vez.

<hr>

#### Varredura por Perfil (`autorecon scan`)

Para executar múltiplas ferramentas em sequência de forma automática, use o comando `scan`:

    sudo autorecon scan --target <ALVO> --profile <PERFIL>

**Exemplos:**

```bash
# Varredura de aplicação web (nmap + nikto + nuclei)
sudo autorecon scan --target 192.168.1.10 --profile web-app

# Reconhecimento de rede (descoberta de hosts, serviços e SO)
sudo autorecon scan --target 192.168.1.0/24 --profile network-recon

# Varredura completa com todas as ferramentas
sudo autorecon scan --target exemplo.com --profile full-recon

# Salvar relatório em caminho personalizado
sudo autorecon scan --target 10.0.0.1 --profile web-app --output ~/relatorios/recon.md
```

O relatório Markdown é salvo automaticamente em `output/report_<perfil>_<alvo>.md`.

<hr>

#### Listar perfis disponíveis

    sudo autorecon profiles

Saída esperada:

```
Perfis disponíveis:

  web-app              Aplicação Web — Reconhecimento focado em HTTP/HTTPS.
                       5 etapas

  network-recon        Reconhecimento de Rede — Descoberta de hosts e serviços.
                       4 etapas

  full-recon           Reconhecimento Completo — Varredura abrangente multi-ferramenta.
                       12 etapas
```

<hr>

#### Perfis incluídos

| Perfil | Ferramentas | Etapas |
|--------|-------------|--------|
| `web-app` | nmap, nikto, nuclei | 5 |
| `network-recon` | nmap | 4 |
| `full-recon` | nmap, nikto, nuclei, wpscan | 12 |

<hr>

#### Criar um perfil personalizado

Crie um arquivo `.yaml` em `profiles/` seguindo a estrutura abaixo:

```yaml
name: meu-perfil
label: Meu Perfil
description: Descrição do que este perfil faz.
steps:
  - tool: nmap
    mode: service_detection
    label: Detecção de Serviços

  - tool: nikto
    mode: vuln_checks
    label: Nikto — Verificações de Vulnerabilidades
```

Os valores aceitos em `tool` e `mode` correspondem aos arquivos em `tools/definitions/`.
  
<hr>

#### Lançador no menu do sistema

O AutoRecon pode ser adicionado ao menu de aplicativos do seu ambiente gráfico como um atalho com ícone pré-configurado.

Para criar o lançador:

    bash launcher/create_launcher.sh

Para remover o lançador:

    bash launcher/remove_launcher.sh

> [!WARNING]
> Compatível com GNOME, KDE, XFCE, LXDE, MATE, Cinnamon e Hyprland. É recomendado instalar em `~/AutoRecon` para garantir o funcionamento correto do atalho.

<hr>

## Apoio ao Projeto

Se você quiser contribuir com o AutoRecon, sinta-se à vontade para abrir uma **Issue** ou criar um **Pull Request** neste repositório.

> 📌 Para manter a organização e o padrão do projeto, siga os templates disponíveis em:
> 
> - [Template de Pull Request](.github/PULL_REQUEST_TEMPLATE.md)
> - [Template de Reporte de Bug](.github/ISSUE_TEMPLATE.md)
> - [Template de Solicitação de Funcionalidade](.github/FEATURE_REQUEST_TEMPLATE.md)

Leia atentamente cada template antes de enviar uma PR, ISSUE ou solicitar uma funcionalidade nova para a ferramenta.

---

Quer apoiar ainda mais? Faça uma doação e ajude a manter este projeto vivo!

**BTC Wallet**:  
`bc1qfy534ujs9yekwthe063fck0zf7hel7paem6sxl`

---

Este projeto está licenciado sob a **GNU Affero General Public License v3.0 (Modificada)**
