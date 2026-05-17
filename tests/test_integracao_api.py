"""
Testes de Integração — MedLembrete × RxNorm API (NIH)

Valida que o módulo api_remedios.py:
  1. Parseia corretamente a resposta real da API (via mock de rede).
  2. Lida com medicamento não encontrado.
  3. Lança ErroAPI em falhas de rede.
  4. Retorna a estrutura esperada na resposta.

Os mocks evitam dependência de rede real durante o CI,
garantindo testes rápidos, determinísticos e sem limite de requisições.
"""

import json
from io import BytesIO
from unittest.mock import patch, MagicMock

import pytest

from src.api_remedios import buscar_info_medicamento, buscar_interacoes, ErroAPI


# ──────────────────────────────────────────────────────────────────────────────
# Helpers — payloads fictícios que imitam a estrutura real da RxNorm API
# ──────────────────────────────────────────────────────────────────────────────

PAYLOAD_METFORMINA = {
    "drugGroup": {
        "name": "metformin",
        "conceptGroup": [
            {
                "tty": "IN",
                "conceptProperties": [
                    {"rxcui": "6809", "name": "metFORMIN", "synonym": ""},
                    {"rxcui": "6809", "name": "Metformin hydrochloride", "synonym": ""},
                ],
            }
        ],
    }
}

PAYLOAD_VAZIO = {
    "drugGroup": {
        "name": "xyz_nao_existe",
        "conceptGroup": [{"tty": "IN"}],  # sem 'conceptProperties'
    }
}

PAYLOAD_INTERACOES = {
    "interactionTypeGroup": [
        {
            "sourceDisclaimer": "...",
            "interactionType": [
                {
                    "comment": "...",
                    "interactionPair": [
                        {
                            "interactionConcept": [],
                            "severity": "high",
                            "description": "Metformin may interact with alcohol.",
                        }
                    ],
                }
            ],
        }
    ]
}

PAYLOAD_SEM_INTERACOES = {"interactionTypeGroup": []}


def _mock_urlopen(payload: dict):
    """Retorna um context manager que simula urllib.request.urlopen."""
    corpo = json.dumps(payload).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.read.return_value = corpo
    return mock_resp


# ──────────────────────────────────────────────────────────────────────────────
# Testes de buscar_info_medicamento
# ──────────────────────────────────────────────────────────────────────────────


class TestBuscarInfoMedicamento:
    def test_retorna_dict_com_campos_esperados(self):
        """Caminho feliz: API retorna dados válidos e o dict tem todos os campos."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_METFORMINA)):
            info = buscar_info_medicamento("metformin")

        assert info is not None
        assert "rxcui" in info
        assert "nome_oficial" in info
        assert "sinonimos" in info

    def test_rxcui_correto(self):
        """O RxCUI retornado deve corresponder ao primeiro conceito da resposta."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_METFORMINA)):
            info = buscar_info_medicamento("metformin")

        assert info["rxcui"] == "6809"

    def test_nome_oficial_correto(self):
        """O nome oficial deve vir do campo 'name' do primeiro conceito."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_METFORMINA)):
            info = buscar_info_medicamento("metformin")

        assert info["nome_oficial"] == "metFORMIN"

    def test_sinonimos_sao_lista(self):
        """O campo sinonimos deve ser sempre uma lista (mesmo que vazia)."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_METFORMINA)):
            info = buscar_info_medicamento("metformin")

        assert isinstance(info["sinonimos"], list)

    def test_medicamento_nao_encontrado_retorna_none(self):
        """Se a API não retornar conceptProperties, a função deve retornar None."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_VAZIO)):
            info = buscar_info_medicamento("xyz_nao_existe")

        assert info is None

    def test_nome_vazio_lanca_value_error(self):
        """Nome em branco deve lançar ValueError antes de chamar a API."""
        with pytest.raises(ValueError, match="vazio"):
            buscar_info_medicamento("   ")

    def test_falha_de_rede_lanca_erro_api(self):
        """Falha de conexão deve ser convertida em ErroAPI."""
        import urllib.error

        with patch(
            "src.api_remedios.urllib.request.urlopen",
            side_effect=urllib.error.URLError("timed out"),
        ):
            with pytest.raises(ErroAPI, match="Falha de conexão"):
                buscar_info_medicamento("aspirin")

    def test_http_error_lanca_erro_api(self):
        """Erro HTTP (ex: 500) deve ser convertido em ErroAPI."""
        import urllib.error

        with patch(
            "src.api_remedios.urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(None, 500, "Server Error", {}, None),
        ):
            with pytest.raises(ErroAPI, match="Erro HTTP"):
                buscar_info_medicamento("aspirin")

    def test_json_invalido_lanca_erro_api(self):
        """Resposta com JSON malformado deve lançar ErroAPI."""
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.read.return_value = b"isso nao e json {"

        with patch("src.api_remedios.urllib.request.urlopen", return_value=mock_resp):
            with pytest.raises(ErroAPI, match="JSON"):
                buscar_info_medicamento("aspirin")


# ──────────────────────────────────────────────────────────────────────────────
# Testes de buscar_interacoes
# ──────────────────────────────────────────────────────────────────────────────


class TestBuscarInteracoes:
    def test_retorna_lista_de_strings(self):
        """Caminho feliz: interações retornadas como lista de strings."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_INTERACOES)):
            resultado = buscar_interacoes("6809")

        assert isinstance(resultado, list)
        assert len(resultado) == 1
        assert "alcohol" in resultado[0].lower()

    def test_sem_interacoes_retorna_lista_vazia(self):
        """Se não houver interações, deve retornar lista vazia (não None)."""
        with patch("src.api_remedios.urllib.request.urlopen", return_value=_mock_urlopen(PAYLOAD_SEM_INTERACOES)):
            resultado = buscar_interacoes("9999")

        assert resultado == []

    def test_falha_de_rede_lanca_erro_api(self):
        """Falha de rede deve lançar ErroAPI."""
        import urllib.error

        with patch(
            "src.api_remedios.urllib.request.urlopen",
            side_effect=urllib.error.URLError("timeout"),
        ):
            with pytest.raises(ErroAPI):
                buscar_interacoes("6809")
