💊 MedLembrete
![CI](https://github.com/SEU_USUARIO/medlembrete/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![Licença](https://img.shields.io/badge/licença-MIT-green)
> CLI em Python para controle de medicamentos e registro de doses — feito para idosos, cuidadores e pacientes crônicos.
---
🌐 Deploy (Entrega Intermediária)
> 👉 **[Executar no Replit](https://replit.com/@SEU_USUARIO/MedLembrete)** ← substitua pelo link após publicar
Para CLIs Python, o deploy recomendado é via:
Replit — execução online, gratuita, sem configuração
GitHub Codespaces — ambiente de dev no browser
Docker Hub — imagem pública para qualquer máquina
---
🎯 Problema Real
Idosos e pacientes crônicos frequentemente precisam tomar múltiplos medicamentos em horários distintos. Esquecer ou confundir doses pode resultar em internações ou interações medicamentosas graves.
💡 Proposta de Solução
MedLembrete é uma CLI que permite:
Cadastrar medicamentos com nome, dose e horário prescrito
Registrar quando cada dose foi tomada (com timestamp)
Consultar histórico de doses por medicamento
Remover medicamentos
[NOVO v1.1] Consultar informações oficiais e interações via RxNorm API (NIH)
🔌 Integração com API Pública — RxNorm (NIH/NLM)
A entrega intermediária adiciona integração com a RxNorm REST API, API gratuita e aberta do National Library of Medicine dos EUA.
Endpoints utilizados:
`GET /REST/drugs.json?name={nome}` — nome oficial, RxCUI, sinônimos
`GET /REST/interaction/interaction.json?rxcui={id}` — interações medicamentosas
Exemplo de uso (opção 6 no menu):
```
Escolha uma opção: 6
Nome do medicamento para consultar na RxNorm (NIH): metformin

📋 Nome oficial : metFORMIN
   RxCUI        : 6809
   Sinônimos     : Metformin hydrochloride

⚠️  Interações encontradas:
   • Metformin may interact with alcohol.
```
> Sem necessidade de chave de API. 100% gratuita e aberta.
✨ Funcionalidades
#	Funcionalidade	Descrição
1	Cadastrar medicamento	Nome, dose e horário prescrito
2	Listar medicamentos	Exibe todos os remédios cadastrados
3	Registrar dose tomada	Salva data e hora exata
4	Histórico de doses	Lista registros com filtro
5	Remover medicamento	Remove um cadastro
6	Consultar bula (RxNorm)	Busca info e interações via API
🚀 Instalação
```bash
git clone https://github.com/SEU_USUARIO/membres-entrega.git
cd membres-entrega
pip install ".[dev]"
python src/app.py
```
🧪 Testes
```bash
pytest --cov=src --cov-report=term-missing
```
Inclui testes unitários + testes de integração com mock da API. Total: 30+ testes.
📁 Estrutura
```
membres-entrega/
├── src/
│   ├── app.py              # CLI principal (opção 6 nova)
│   └── api_remedios.py     # Módulo RxNorm API  ← NOVO
├── tests/
│   ├── test_app.py         # Testes unitários
│   └── test_integracao_api.py  # Testes de integração  ← NOVO
├── .github/workflows/ci.yml
└── pyproject.toml
```
📌 Changelog
v1.1.0 — Entrega Intermediária
Integração com RxNorm API (NIH/NLM)
Módulo `src/api_remedios.py` com `buscar_info_medicamento` e `buscar_interacoes`
Opção 6 no menu CLI
Testes de integração com mocking completo
Deploy documentado
v1.0.0 — Entrega Inicial
CRUD de medicamentos e histórico de doses
👤 Autor
Seu Nome — @helgafell-sys
📄 Licença MIT
