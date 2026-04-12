# 💊 MedLembrete

![CI](https://github.com/SEU_USUARIO/medlembrete/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![Licença](https://img.shields.io/badge/licença-MIT-green)

> CLI em Python para controle de medicamentos e registro de doses — feito para idosos, cuidadores e pacientes crônicos.

---

## 🎯 Problema Real

Idosos e pacientes com doenças crônicas frequentemente precisam tomar múltiplos medicamentos em horários distintos. Esquecer ou confundir doses é um dos erros mais comuns no autocuidado em saúde, podendo resultar em internações, agravamento de quadros clínicos ou interações medicamentosas graves. Cuidadores informais (familiares, por exemplo) também lidam com a difícil tarefa de acompanhar e registrar o que foi tomado.

## 💡 Proposta de Solução

**MedLembrete** é uma aplicação de linha de comando (CLI) que permite:

- Cadastrar medicamentos com nome, dose e horário prescrito;
- Registrar, com timestamp, quando cada dose foi tomada;
- Consultar o histórico de doses por medicamento;
- Remover medicamentos que não são mais necessários.

A persistência é feita em um arquivo JSON local, sem necessidade de banco de dados ou conexão com a internet.

## 👥 Público-Alvo

- Idosos que gerenciam seus próprios medicamentos;
- Cuidadores familiares ou profissionais;
- Pacientes com doenças crônicas (hipertensão, diabetes, etc.);
- Qualquer pessoa que precise de um registro simples de rotina medicamentosa.

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Cadastrar medicamento | Nome, dose e horário prescrito |
| Listar medicamentos | Exibe todos os remédios cadastrados |
| Registrar dose tomada | Salva data e hora exata da tomada |
| Histórico de doses | Lista registros, com filtro opcional por remédio |
| Remover medicamento | Remove o cadastro de um remédio |

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** — linguagem principal
- **JSON** — armazenamento local dos dados
- **pytest** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/medlembrete.git
cd medlembrete

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

Você verá o menu interativo:

```
╔══════════════════════════════════╗
║        💊 MedLembrete 1.0.0       ║
╠══════════════════════════════════╣
║  1. Cadastrar medicamento        ║
║  2. Listar medicamentos          ║
║  3. Registrar dose tomada        ║
║  4. Ver histórico de doses       ║
║  5. Remover medicamento          ║
║  0. Sair                         ║
╚══════════════════════════════════╝
```

### Exemplo de uso

```
Escolha uma opção: 1
Nome do medicamento: Losartana
Horário (HH:MM): 08:00
Dose (ex: 50mg): 50mg
✅ 'Losartana' cadastrado com sucesso!

Escolha uma opção: 3
Nome do medicamento tomado: Losartana
✅ Dose de 'Losartana' registrada em 2025-06-01 às 08:03:42.
```

## 🧪 Executar os Testes

```bash
pytest
```

Para ver a cobertura de código:

```bash
pytest --cov=src --cov-report=term-missing
```

Saída esperada: **20+ testes**, todos passando.

## 🔍 Executar o Lint

```bash
ruff check src/ tests/
```

Se não houver problemas, não haverá saída. Para corrigir automaticamente:

```bash
ruff check --fix src/ tests/
```

## 📁 Estrutura do Projeto

```
medlembrete/
├── src/
│   ├── __init__.py
│   └── app.py              # Lógica principal + CLI
├── tests/
│   ├── __init__.py
│   └── test_app.py         # Testes automatizados
├── data/                   # Criado automaticamente na primeira execução
│   └── medicamentos.json
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI
├── pyproject.toml          # Versão, dependências e configurações
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── README.md
```

## 📌 Versão

**1.0.0** — Versão inicial com funcionalidades de cadastro, registro de doses e histórico.

Veja o histórico completo em [CHANGELOG.md](CHANGELOG.md).

## 👤 Autor

**Seu Nome**
- GitHub: [@SEU_USUARIO](https://github.com/SEU_USUARIO)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
