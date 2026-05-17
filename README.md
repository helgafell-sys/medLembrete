# 💊 MedLembrete

![CI](https://github.com/helgafell-sys/medLembrete/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![Licença](https://img.shields.io/badge/licença-MIT-green)

> CLI em Python para controle de medicamentos e registro de doses — feito para idosos, cuidadores e pacientes crônicos.

---

## 🌐 Deploy

> 👉 **https://medlembrete-8swl.onrender.com**

A aplicação está publicada na plataforma **Render**. Por se tratar de uma CLI interativa, para executá-la siga as instruções em [Instalação](#-instalação).

---

## 🎯 Problema Real

Idosos e pacientes com doenças crônicas frequentemente precisam tomar múltiplos medicamentos em horários distintos. Esquecer ou confundir doses é um dos erros mais comuns no autocuidado em saúde, podendo resultar em internações, agravamento de quadros clínicos ou interações medicamentosas graves. Cuidadores informais (familiares, por exemplo) também lidam com a difícil tarefa de acompanhar e registrar o que foi tomado.

## 💡 Proposta de Solução

**MedLembrete** é uma aplicação de linha de comando (CLI) que permite:

- Cadastrar medicamentos com nome, dose e horário prescrito
- Registrar, com timestamp, quando cada dose foi tomada
- Consultar o histórico de doses por medicamento
- Remover medicamentos que não são mais necessários
- **[NOVO v1.1]** Consultar informações oficiais e interações via **RxNorm API (NIH)**

## 👥 Público-Alvo

- Idosos que gerenciam seus próprios medicamentos
- Cuidadores familiares ou profissionais
- Pacientes com doenças crônicas (hipertensão, diabetes, etc.)
- Qualquer pessoa que precise de um registro simples de rotina medicamentosa

## ✨ Funcionalidades

| # | Funcionalidade | Descrição |
|---|---|---|
| 1 | Cadastrar medicamento | Nome, dose e horário prescrito |
| 2 | Listar medicamentos | Exibe todos os remédios cadastrados |
| 3 | Registrar dose tomada | Salva data e hora exata da tomada |
| 4 | Histórico de doses | Lista registros, com filtro opcional por remédio |
| 5 | Remover medicamento | Remove o cadastro de um remédio |
| 6 | **Consultar bula (RxNorm)** | **Busca nome oficial, RxCUI e interações via API do NIH** |

## 🔌 Integração com API Pública — RxNorm (NIH/NLM)

A **entrega intermediária** adiciona integração com a [RxNorm REST API](https://rxnav.nlm.nih.gov/RxNormAPIs.html), API **gratuita e aberta** do *National Library of Medicine* dos EUA.

**Endpoints utilizados:**
- `GET /REST/drugs.json?name={nome}` — nome oficial, RxCUI e sinônimos
- `GET /REST/interaction/interaction.json?rxcui={id}` — interações medicamentosas

**Exemplo de uso (opção 6 no menu):**
```
Escolha uma opção: 6
Nome do medicamento para consultar na RxNorm (NIH): metformin

🔍 Consultando RxNorm para 'metformin'…

📋 Nome oficial : metFORMIN
   RxCUI        : 6809
   Sinônimos     : Metformin hydrochloride

⚠️  Interações encontradas:
   • Metformin may interact with alcohol.
```

> Sem necessidade de chave de API. 100% gratuita e aberta.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** — linguagem principal
- **JSON** — armazenamento local dos dados
- **urllib** — consumo da API REST (biblioteca padrão, sem dependências extras)
- **pytest** — testes unitários e de integração
- **unittest.mock** — mocking da API para testes determinísticos
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)
- **Render** — hospedagem em nuvem

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/helgafell-sys/medLembrete.git
cd medLembrete

# 2. (Opcional) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Instale as dependências de desenvolvimento
pip install ".[dev]"
```

## ▶️ Execução

```bash
python src/app.py
```

Menu interativo:

```
╔══════════════════════════════════╗
║        💊 MedLembrete 1.1.0       ║
╠══════════════════════════════════╣
║  1. Cadastrar medicamento        ║
║  2. Listar medicamentos          ║
║  3. Registrar dose tomada        ║
║  4. Ver histórico de doses       ║
║  5. Remover medicamento          ║
║  6. Consultar bula (RxNorm/NIH)  ║
║  0. Sair                         ║
╚══════════════════════════════════╝
```

## 🧪 Executar os Testes

```bash
pytest --cov=src --cov-report=term-missing
```

Inclui **testes unitários** (`tests/test_app.py`) e **testes de integração** (`tests/test_integracao_api.py`), totalizando **33 testes** com 96% de cobertura.

## 🔍 Executar o Lint

```bash
ruff check src/ tests/
```

## 📁 Estrutura do Projeto

```
medLembrete/
├── src/
│   ├── __init__.py
│   ├── app.py                  # Lógica principal + CLI
│   └── api_remedios.py         # Módulo de integração RxNorm ← NOVO
├── tests/
│   ├── __init__.py
│   ├── test_app.py             # Testes unitários (21 testes)
│   └── test_integracao_api.py  # Testes de integração (12 testes) ← NOVO
├── data/                       # Criado automaticamente na 1ª execução
│   └── medicamentos.json
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI
├── pyproject.toml
└── README.md
```

## 📌 Changelog

### v1.1.0 — Entrega Intermediária
- Integração com RxNorm API (NIH/NLM)
- Novo módulo `src/api_remedios.py`
- Opção 6 no menu CLI: consultar bula e interações
- 12 testes de integração com mocking (`tests/test_integracao_api.py`)
- Deploy publicado no Render: https://medlembrete-8swl.onrender.com

### v1.0.0 — Entrega Inicial
- Cadastro, listagem, registro de doses, histórico e remoção
- Persistência em JSON local
- CI com GitHub Actions

## 👤 Autor

**Seu Nome**
- GitHub: [@helgafell-sys](https://github.com/helgafell-sys)

## 📄 Licença

Este projeto está sob a licença MIT.
