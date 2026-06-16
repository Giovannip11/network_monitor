# Network Monitor 🔍🌐

Um monitor de rede automatizado desenvolvido em Python para ambientes locais. O sistema realiza varreduras periódicas em uma sub-rede configurada, detecta dispositivos conectados, identifica seus respectivos Sistemas Operacionais, fabricantes (através do endereço MAC) e portas ativas. 

Os dados coletados são estruturados de forma relacional e armazenados localmente em um banco de dados SQLite, permitindo rastrear o histórico de conexões e gerando automaticamente relatórios consolidados em formato PDF a cada ciclo.

---

##  Funcionalidades

- **Varredura Paralelizada:** Utiliza `ThreadPoolExecutor` para acelerar o escaneamento de múltiplos hosts simultaneamente através do Nmap.
- **Identificação de Ativos:** Detecta IP, MAC Address, Fabricante (Vendor) e Sistema Operacional (OS).
- **Persistência em SQLite:** Armazenamento relacional e histórico completo de varreduras para auditoria de segurança ou inventário de TI.
- **Detecção de Mudanças em Tempo Real:** Identifica e loga novos dispositivos que entraram na rede ou dispositivos que ficaram offline.
- **Relatórios Automatizados:** Geração contínua de relatórios em PDF detalhados com os dados coletados na última varredura.

---

##  Estrutura do Projeto

```text
network_monitor/
├── app/
│   ├── config.py          # Centralização de caminhos e diretórios
│   ├── logger.py          # Gerenciamento de logs do sistema (.log)
│   ├── main.py            # Orquestrador do loop principal do monitor
│   ├── monitor.py         # Lógica de comparação entre varreduras (Novos/Offline)
│   ├── pdf_report.py      # Geração de relatórios com ReportLab
│   ├── scanner.py         # Mecanismo de varredura utilizando python-nmap e socket
│   ├── storage.py         # Conexão, inicialização e queries do banco SQLite
│   └── utils.py           # Regras de detecção de tipo de dispositivo e portas
├── data/
│   └── network_monitor.db # Banco de dados SQLite (Gerado automaticamente)
├── history/
│   └── relatorio_*.pdf    # Histórico de PDFs gerados (Gerado automaticamente)
├── logs/
│   └── monitor.log        # Registro de eventos textuais (Gerado automaticamente)
├── .env                   # Variáveis de ambiente (Configuração da rede)
└── requirements.txt       # Dependências do projeto
```
## Pré-requisitos
-  Python 3.10 ou superior
-  NMAP, o core do scanner depende do binário do NMAP instalado no sistema operacional

