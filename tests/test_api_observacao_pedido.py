import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_deve_adicionar_observacao(client):
    client.post("/clientes", json={"cpf": "12345678900", "nome": "João"})
    client.post("/produtos", json={"codigo": 1, "valor": 10.0, "tipo": 1, "desconto_percentual": 0})
    r = client.post("/lanchonete/pedidos", json={"cpf": "12345678900", "cod_produto": 1, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]

    response = client.post(
        f"/lanchonete/pedidos/{cod_pedido}/observacao",
        json={
            "observacao": "Sem cebola"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] == True
    assert data["mensagem"] == "Observação adicionada com sucesso"


def test_nao_deve_aceitar_observacao_vazia(client):
    client.post("/clientes", json={"cpf": "12345678903", "nome": "Ana"})
    client.post("/produtos", json={"codigo": 4, "valor": 10.0, "tipo": 1, "desconto_percentual": 0})
    r = client.post("/lanchonete/pedidos", json={"cpf": "12345678903", "cod_produto": 4, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]

    response = client.post(
        f"/lanchonete/pedidos/{cod_pedido}/observacao",
        json={
            "observacao": ""
        }
    )

    assert response.status_code == 400


def test_nao_deve_adicionar_observacao_em_pedido_finalizado(client):
    client.post("/clientes", json={"cpf": "12345678901", "nome": "Maria"})
    client.post("/produtos", json={"codigo": 2, "valor": 15.0, "tipo": 1, "desconto_percentual": 0})
    r = client.post("/lanchonete/pedidos", json={"cpf": "12345678901", "cod_produto": 2, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]
    client.post(f"/lanchonete/pedidos/{cod_pedido}/finalizar")

    response = client.post(
        f"/lanchonete/pedidos/{cod_pedido}/observacao",
        json={
            "observacao": "Sem molho"
        }
    )

    assert response.status_code == 400


def test_deve_buscar_observacao_pedido(client):
    client.post("/clientes", json={"cpf": "12345678902", "nome": "Pedro"})
    client.post("/produtos", json={"codigo": 3, "valor": 20.0, "tipo": 1, "desconto_percentual": 0})
    r = client.post("/lanchonete/pedidos", json={"cpf": "12345678902", "cod_produto": 3, "qtd_max_produtos": 5})
    cod_pedido = r.json()["codigo"]
    client.post(
        f"/lanchonete/pedidos/{cod_pedido}/observacao",
        json={
            "observacao": "Sem cebola e sem molho"
        }
    )

    response = client.get(
        f"/lanchonete/pedidos/{cod_pedido}/observacao"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["codigo"] == cod_pedido
    assert data["observacao"] == "Sem cebola e sem molho"