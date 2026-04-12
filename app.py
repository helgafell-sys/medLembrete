"""
MedLembrete - Controle de Medicamentos via CLI
Ajuda idosos, cuidadores e pacientes crônicos a gerenciar
remédios e registrar doses tomadas.
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "medicamentos.json")


def _carregar_dados() -> dict:
    """Carrega dados do arquivo JSON. Retorna estrutura vazia se não existir."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return {"medicamentos": [], "historico": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_dados(dados: dict) -> None:
    """Persiste os dados no arquivo JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def cadastrar_medicamento(nome: str, horario: str, dose: str) -> dict:
    """
    Cadastra um novo medicamento.

    Args:
        nome: Nome do medicamento (ex: 'Losartana').
        horario: Horário de toma no formato HH:MM (ex: '08:00').
        dose: Dose a ser tomada (ex: '50mg').

    Returns:
        Dicionário com os dados do medicamento cadastrado.

    Raises:
        ValueError: Se algum argumento for inválido.
    """
    nome = nome.strip()
    horario = horario.strip()
    dose = dose.strip()

    if not nome:
        raise ValueError("O nome do medicamento não pode ser vazio.")
    if not dose:
        raise ValueError("A dose não pode ser vazia.")
    if not _validar_horario(horario):
        raise ValueError(f"Horário inválido: '{horario}'. Use o formato HH:MM (ex: 08:00).")

    dados = _carregar_dados()

    for med in dados["medicamentos"]:
        if med["nome"].lower() == nome.lower():
            raise ValueError(f"Medicamento '{nome}' já cadastrado.")

    medicamento = {
        "id": len(dados["medicamentos"]) + 1,
        "nome": nome,
        "horario": horario,
        "dose": dose,
        "criado_em": datetime.now().isoformat(),
    }
    dados["medicamentos"].append(medicamento)
    _salvar_dados(dados)
    return medicamento


def listar_medicamentos() -> list:
    """Retorna a lista de todos os medicamentos cadastrados."""
    dados = _carregar_dados()
    return dados["medicamentos"]


def registrar_dose(nome: str) -> dict:
    """
    Registra que uma dose do medicamento foi tomada agora.

    Args:
        nome: Nome do medicamento.

    Returns:
        Dicionário com o registro da dose.

    Raises:
        ValueError: Se o medicamento não existir.
    """
    nome = nome.strip()
    dados = _carregar_dados()

    med = next(
        (m for m in dados["medicamentos"] if m["nome"].lower() == nome.lower()),
        None,
    )
    if not med:
        raise ValueError(f"Medicamento '{nome}' não encontrado.")

    registro = {
        "medicamento": med["nome"],
        "dose": med["dose"],
        "tomado_em": datetime.now().isoformat(),
    }
    dados["historico"].append(registro)
    _salvar_dados(dados)
    return registro


def historico_doses(nome: str | None = None) -> list:
    """
    Retorna o histórico de doses tomadas.

    Args:
        nome: Filtra por medicamento específico. Se None, retorna tudo.

    Returns:
        Lista de registros de doses.
    """
    dados = _carregar_dados()
    historico = dados["historico"]
    if nome:
        historico = [h for h in historico if h["medicamento"].lower() == nome.lower()]
    return historico


def remover_medicamento(nome: str) -> dict:
    """
    Remove um medicamento pelo nome.

    Args:
        nome: Nome do medicamento a remover.

    Returns:
        Dicionário com os dados do medicamento removido.

    Raises:
        ValueError: Se o medicamento não for encontrado.
    """
    nome = nome.strip()
    dados = _carregar_dados()

    med = next(
        (m for m in dados["medicamentos"] if m["nome"].lower() == nome.lower()),
        None,
    )
    if not med:
        raise ValueError(f"Medicamento '{nome}' não encontrado.")

    dados["medicamentos"] = [
        m for m in dados["medicamentos"] if m["nome"].lower() != nome.lower()
    ]
    _salvar_dados(dados)
    return med


def _validar_horario(horario: str) -> bool:
    """Valida se o horário está no formato HH:MM."""
    try:
        datetime.strptime(horario, "%H:%M")
        return True
    except ValueError:
        return False


# ──────────────────────────────────────────────
# Interface CLI
# ──────────────────────────────────────────────

MENU = """
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
"""


def _input(prompt: str) -> str:  # pragma: no cover
    return input(prompt)


def _print(msg: str) -> None:  # pragma: no cover
    print(msg)


def run_cli() -> None:  # pragma: no cover
    """Loop principal da interface CLI."""
    while True:
        _print(MENU)
        opcao = _input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = _input("Nome do medicamento: ")
            horario = _input("Horário (HH:MM): ")
            dose = _input("Dose (ex: 50mg): ")
            try:
                med = cadastrar_medicamento(nome, horario, dose)
                _print(f"\n✅ '{med['nome']}' cadastrado com sucesso!")
            except ValueError as e:
                _print(f"\n❌ Erro: {e}")

        elif opcao == "2":
            meds = listar_medicamentos()
            if not meds:
                _print("\nNenhum medicamento cadastrado.")
            else:
                _print("\n📋 Medicamentos cadastrados:")
                for m in meds:
                    _print(f"  • {m['nome']} — {m['dose']} às {m['horario']}")

        elif opcao == "3":
            nome = _input("Nome do medicamento tomado: ")
            try:
                reg = registrar_dose(nome)
                horario = reg["tomado_em"][:19].replace("T", " às ")
                _print(f"\n✅ Dose de '{reg['medicamento']}' registrada em {horario}.")
            except ValueError as e:
                _print(f"\n❌ Erro: {e}")

        elif opcao == "4":
            nome = _input("Filtrar por medicamento (Enter para todos): ").strip() or None
            hist = historico_doses(nome)
            if not hist:
                _print("\nNenhuma dose registrada.")
            else:
                _print("\n📅 Histórico de doses:")
                for h in hist:
                    quando = h["tomado_em"][:19].replace("T", " às ")
                    _print(f"  • {h['medicamento']} ({h['dose']}) — {quando}")

        elif opcao == "5":
            nome = _input("Nome do medicamento a remover: ")
            try:
                med = remover_medicamento(nome)
                _print(f"\n🗑️  '{med['nome']}' removido com sucesso.")
            except ValueError as e:
                _print(f"\n❌ Erro: {e}")

        elif opcao == "0":
            _print("\nAté logo! Não esqueça seus remédios. 💊")
            break

        else:
            _print("\n⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":  # pragma: no cover
    run_cli()
