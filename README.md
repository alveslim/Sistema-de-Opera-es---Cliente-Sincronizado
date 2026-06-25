# 📑 Gerador de Ordens de Produção (PrismaSystem)

O **PrismaSystem** é um aplicativo desktop moderno desenvolvido em Python para otimizar o cadastro, gerenciamento e emissão de Ordens de Produção (OPs). Com uma interface gráfica intuitiva, o sistema automatiza tarefas repetitivas, gera relatórios em PDF legítimos e envia documentos direto para a fila de impressão do sistema operacional.

---

## 🚀 Funcionalidades Principais

* **🎨 Interface Gráfica Moderna (GUI):** Construída com `CustomTkinter`, oferecendo suporte nativo ao modo escuro/claro (*Dark/Light Mode*) integrado ao sistema operacional.
* **🔢 Numeração Automatizada:** Consulta inteligente ao histórico de registros (`ops.csv`) para sugerir automaticamente o próximo número de OP disponível.
* **💾 Exportação Dupla:**
* **Planilhas (CSV):** Armazenamento estruturado dos dados para controle interno ou integração com Excel.
* **Relatórios (PDF):** Geração de documentos PDF legítimos, limpos e bem estruturados utilizando a biblioteca `ReportLab`.


* **🖨️ Impressão Silenciosa (One-Click):** Envio direto do documento para a impressora padrão do Windows ou Linux, rodando em segundo plano sem travar a interface do usuário.

---

## 🛠️ Tecnologias e Bibliotecas

* **[Python 3.x](https://www.python.org/)** — Linguagem base do projeto.
* **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — Interface visual moderna e responsiva.
* **[ReportLab](https://www.reportlab.com/)** — Engine de renderização de arquivos PDF de alta qualidade.
* **[PyWin32](https://github.com/mhammond/pywin32)** — Integração com a API nativa do Windows para gerenciamento de filas de impressão.

---

## 🗂️ Estrutura do Projeto

O sistema foi arquitetado seguindo boas práticas de divisão de responsabilidades:

* `main.py`: Gerencia a janela, os elementos visuais (inputs/botões) e os eventos de clique.
* `banco_dados.py`: Responsável pela leitura/escrita no arquivo CSV, geração do PDF e comunicação com o hardware de impressão.
* `modelos.py`: Contém a classe `OrdemProducao`, abstraindo as regras de negócio e a conversão de estruturas de dados.

---

## 📋 Pré-requisitos e Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/alveslim/PrismaSystem.git
cd PrismaSystem

```

### 2. Configurar o Ambiente Virtual (Recomendado)

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Ativar no Linux/Mac
source .venv/bin/activate

```

### 3. Instalar as Dependências

Com o ambiente ativado, instale os pacotes necessários:

```bash
pip install customtkinter reportlab pywin32

```

### 4. Executar o Aplicativo

```bash
python archivementMain/main.py

```

---

## 🤝 Como Contribuir

1. Faça um **Fork** do projeto.
2. Crie uma nova Branch para sua funcionalidade (`git checkout -b feature/NovaFuncionalidade`).
3. Faça o **Commit** de suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Envie para a Branch original (`git push origin feature/NovaFuncionalidade`).
5. Abra um **Pull Request**.
