"""
api_remedios.py — Integração com a RxNorm API (NIH/NLM)

A RxNorm é uma API pública e gratuita do National Library of Medicine (EUA)
que fornece informações normalizadas sobre medicamentos, incluindo nome oficial,
código RxCUI e classe terapêutica.

Documentação: https://rxnav.nlm.nih.gov/RxNormAPIs.html
"""

import urllib.request
import urllib.error
import urllib.parse
import json
from typing import Optional

BASE_URL = "https://rxnav.nlm.nih.gov/REST"
TIMEOUT_SEGUNDOS = 10


class ErroAPI(Exception):
    """Lançada quando a comunicação com a API externa falha."""


def buscar_info_medicamento(nome: str) -> Optional[dict]:
    """
    Busca informações sobre um medicamento pelo nome na API RxNorm (NIH).

    Args:
        nome: Nome do medicamento (ex: 'aspirin', 'metformin').

    Returns:
        Dicionário com campos 'rxcui', 'nome_oficial' e 'sinonimos',
        ou None se o medicamento não for encontrado.

    Raises:
        ErroAPI: Se houver falha de rede ou resposta inválida da API.
    """
    nome = nome.strip()
    if not nome:
        raise ValueError("O nome do medicamento não pode ser vazio.")

    # Endpoint: busca aproximada por nome
    url = f"{BASE_URL}/drugs.json?name={urllib.parse.quote(nome)}"

    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SEGUNDOS) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ErroAPI(f"Erro HTTP {exc.code} ao consultar RxNorm.") from exc
    except urllib.error.URLError as exc:
        raise ErroAPI(f"Falha de conexão com RxNorm: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise ErroAPI("Resposta inválida (JSON malformado) da RxNorm.") from exc

    # Navega na estrutura de resposta da API
    grupo = dados.get("drugGroup", {})
    conceitos = grupo.get("conceptGroup", [])

    for grupo_conceito in conceitos:
        itens = grupo_conceito.get("conceptProperties", [])
        if itens:
            primeiro = itens[0]
            return {
                "rxcui": primeiro.get("rxcui", ""),
                "nome_oficial": primeiro.get("name", nome),
                "sinonimos": [i.get("name", "") for i in itens[1:5]],  # até 4 sinônimos
            }

    return None  # medicamento não encontrado na base da RxNorm


def buscar_interacoes(rxcui: str) -> list[str]:
    """
    Busca possíveis interações medicamentosas para um RxCUI.

    Args:
        rxcui: Código RxCUI do medicamento.

    Returns:
        Lista de strings descrevendo interações encontradas (pode ser vazia).

    Raises:
        ErroAPI: Se houver falha de rede ou resposta inválida da API.
    """
    url = f"{BASE_URL}/interaction/interaction.json?rxcui={urllib.parse.quote(rxcui)}"

    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SEGUNDOS) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ErroAPI(f"Erro HTTP {exc.code} ao consultar interações.") from exc
    except urllib.error.URLError as exc:
        raise ErroAPI(f"Falha de conexão com RxNorm: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise ErroAPI("Resposta inválida (JSON malformado) da RxNorm.") from exc

    interacoes = []
    grupos = dados.get("interactionTypeGroup", [])
    for grupo in grupos:
        for tipo in grupo.get("interactionType", []):
            for par in tipo.get("interactionPair", []):
                descricao = par.get("description", "")
                if descricao:
                    interacoes.append(descricao)

    return interacoes
