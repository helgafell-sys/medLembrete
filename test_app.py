"""
Testes automatizados do MedLembrete.
Cobre caminho feliz, entradas inválidas e casos limite.
"""

import json
import os
import tempfile
import pytest

# Aponta DATA_FILE para um arquivo temporário durante os testes
import src.app as app


@pytest.fixture(autouse=True)
def usar_arquivo_temp(tmp_path, monkeypatch):
    """Redireciona o DATA_FILE para um diretório temporário isolado."""
    data_file = tmp_path / "medicamentos.json"
    monkeypatch.setattr(app, "DATA_FILE", str(data_file))


# ─── Testes de cadastro ───────────────────────────────────────────────────────

class TestCadastrarMedicamento:
    def test_cadastro_valido(self):
        """Caminho feliz: cadastro com dados corretos."""
        med = app.cadastrar_medicamento("Losartana", "08:00", "50mg")
        assert med["nome"] == "Losartana"
        assert med["horario"] == "08:00"
        assert med["dose"] == "50mg"
        assert "criado_em" in med

    def test_medicamento_aparece_na_listagem(self):
        """Depois de cadastrar, deve aparecer na listagem."""
        app.cadastrar_medicamento("Metformina", "07:30", "500mg")
        lista = app.listar_medicamentos()
        nomes = [m["nome"] for m in lista]
        assert "Metformina" in nomes

    def test_nome_vazio_gera_erro(self):
        """Entrada inválida: nome em branco."""
        with pytest.raises(ValueError, match="nome do medicamento"):
            app.cadastrar_medicamento("", "08:00", "50mg")

    def test_dose_vazia_gera_erro(self):
        """Entrada inválida: dose em branco."""
        with pytest.raises(ValueError, match="dose"):
            app.cadastrar_medicamento("Losartana", "08:00", "")

    def test_horario_invalido_gera_erro(self):
        """Entrada inválida: horário fora do formato HH:MM."""
        with pytest.raises(ValueError, match="Horário inválido"):
            app.cadastrar_medicamento("Losartana", "8h00", "50mg")

    def test_horario_25_invalido(self):
        """Caso limite: hora 25 não existe."""
        with pytest.raises(ValueError, match="Horário inválido"):
            app.cadastrar_medicamento("Losartana", "25:00", "50mg")

    def test_cadastro_duplicado_gera_erro(self):
        """Não deve permitir dois medicamentos com o mesmo nome."""
        app.cadastrar_medicamento("Losartana", "08:00", "50mg")
        with pytest.raises(ValueError, match="já cadastrado"):
            app.cadastrar_medicamento("Losartana", "12:00", "25mg")

    def test_cadastro_case_insensitive_duplicado(self):
        """Duplicata deve ser detectada independentemente de maiúsculas."""
        app.cadastrar_medicamento("Losartana", "08:00", "50mg")
        with pytest.raises(ValueError, match="já cadastrado"):
            app.cadastrar_medicamento("losartana", "08:00", "50mg")


# ─── Testes de registro de dose ───────────────────────────────────────────────

class TestRegistrarDose:
    def test_registrar_dose_valida(self):
        """Caminho feliz: registrar dose de medicamento existente."""
        app.cadastrar_medicamento("Atenolol", "06:00", "25mg")
        reg = app.registrar_dose("Atenolol")
        assert reg["medicamento"] == "Atenolol"
        assert reg["dose"] == "25mg"
        assert "tomado_em" in reg

    def test_registrar_dose_medicamento_inexistente(self):
        """Entrada inválida: medicamento não cadastrado."""
        with pytest.raises(ValueError, match="não encontrado"):
            app.registrar_dose("Remédio Fantasma")

    def test_dose_aparece_no_historico(self):
        """Após registrar, o histórico deve conter a entrada."""
        app.cadastrar_medicamento("Omeprazol", "09:00", "20mg")
        app.registrar_dose("Omeprazol")
        hist = app.historico_doses()
        assert any(h["medicamento"] == "Omeprazol" for h in hist)

    def test_multiplas_doses_no_historico(self):
        """Caso limite: registrar a mesma dose várias vezes deve acumular."""
        app.cadastrar_medicamento("Vitamina C", "08:00", "500mg")
        app.registrar_dose("Vitamina C")
        app.registrar_dose("Vitamina C")
        hist = app.historico_doses("Vitamina C")
        assert len(hist) == 2


# ─── Testes de histórico ──────────────────────────────────────────────────────

class TestHistoricoDoses:
    def test_historico_vazio_retorna_lista(self):
        """Caminho feliz: histórico vazio retorna lista vazia, não erro."""
        hist = app.historico_doses()
        assert hist == []

    def test_filtro_por_nome(self):
        """Filtro deve retornar apenas doses do medicamento solicitado."""
        app.cadastrar_medicamento("Dipirona", "12:00", "500mg")
        app.cadastrar_medicamento("Ibuprofeno", "18:00", "400mg")
        app.registrar_dose("Dipirona")
        app.registrar_dose("Ibuprofeno")

        hist_dipirona = app.historico_doses("Dipirona")
        assert len(hist_dipirona) == 1
        assert hist_dipirona[0]["medicamento"] == "Dipirona"


# ─── Testes de remoção ────────────────────────────────────────────────────────

class TestRemoverMedicamento:
    def test_remocao_valida(self):
        """Caminho feliz: remover medicamento existente."""
        app.cadastrar_medicamento("AAS", "08:00", "100mg")
        med = app.remover_medicamento("AAS")
        assert med["nome"] == "AAS"
        assert all(m["nome"] != "AAS" for m in app.listar_medicamentos())

    def test_remocao_inexistente_gera_erro(self):
        """Entrada inválida: tentar remover o que não existe."""
        with pytest.raises(ValueError, match="não encontrado"):
            app.remover_medicamento("Fantasma")


# ─── Testes de validação de horário ──────────────────────────────────────────

class TestValidarHorario:
    def test_horario_valido(self):
        assert app._validar_horario("08:00") is True

    def test_horario_meia_noite(self):
        """Caso limite: 00:00 deve ser aceito."""
        assert app._validar_horario("00:00") is True

    def test_horario_23_59(self):
        """Caso limite: último minuto do dia deve ser aceito."""
        assert app._validar_horario("23:59") is True

    def test_horario_formato_errado(self):
        assert app._validar_horario("8h00") is False

    def test_horario_vazio(self):
        assert app._validar_horario("") is False
