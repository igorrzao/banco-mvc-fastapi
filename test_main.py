from fastapi.testclient import TestClient
from main import app


cliente = TestClient(app)

def test_deposito_valor_negativo():
    resposta = cliente.post("/deposito/Igor/-50")

    dados = resposta.json()

    assert dados["status"] == "erro"
    assert dados["motivo"] == "Valor inserido inválido para depósito."



def test_transferencia_para_si_mesmo():
    resposta = cliente.post("/transferir/Igor/naruto/100/Igor")

    dados = resposta.json()

    assert dados["status"] == "erro"
    assert dados["motivo"] == "O remetente não pode ser igual ao destinatário."



def test_sacar_saldo_insuficiente():
    resposta = cliente.post("/saque/Igor/naruto/99999")

    dados = resposta.json()

    assert dados["status"] == "erro"
    assert dados["motivo"] == "Saldo insuficiente."

