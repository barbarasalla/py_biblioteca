from api import app

# Teste de API

def test_inicio(client):
    response = client.get("/")

    assert response.status_code==200
    assert response.json()== {
        "mensagem": "API da Biblioteca Funcionando!"
    }

def test_criar_livro(client):

    response = client.post("/livros",
                           json={
                               "titulo": "Clean Code",
                               "autor": "Robert C. Martin",
                               "ano": 2008
                           })

    assert response.status_code == 201

    dados = response.json()

    assert dados["titulo"]=="Clean Code"
    assert dados["autor"] == "Robert C. Martin"
    assert dados["ano"] == 2008
    assert dados["id"] is not None

    app.dependency_overrides.clear()

def test_listar_livros(client):

    client.post("/livros",
                json={
                    "titulo": "Clean Code",
                    "autor": "Robert C. Martin",
                    "ano": 2008
                })

    response = client.get("/livros")

    assert response.status_code==200
    dados = response.json()
    assert len(dados) == 1
    assert dados[0]["titulo"] == "Clean Code"

    app.dependency_overrides.clear()

def test_buscar_livro_por_id(client):

    response_criacao = client.post("/livros",
                json={
                    "titulo": "Python Fluente",
                    "autor": "Luciano Ramalho",
                    "ano": 2022
                })

    id_criacao = response_criacao.json()["id"]
    response = client.get(f"/livros/{id_criacao}")

    assert response.status_code==200
    dados = response.json()

    assert dados["id"]==id_criacao

def test_criar_livro_dados_invalidos(client):

    response = client.post(
        "/livros",
        json={
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "ano": "abc"
        }
    )

    assert response.status_code == 422
    app.dependency_overrides.clear()

def test_buscar_livro_inexistente(client):

    response = client.get("/livros/9999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Livro não encontrado"
    }

def test_atualizar_livro(client):

    response_criacao = client.post(
        "/livros",
        json={
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "ano": 2008
        }
    )

    id_livro = response_criacao.json()["id"]

    # Atualiza o livro
    response = client.put(
        f"/livros/{id_livro}",
        json={
            "titulo": "Clean Code - Atualizado",
            "autor": "Robert C. Martin",
            "ano": 2020
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["id"] == id_livro
    assert dados["titulo"] == "Clean Code - Atualizado"
    assert dados["autor"] == "Robert C. Martin"
    assert dados["ano"] == 2020

def testar_atualizar_livro_invalido(client):
    response_criacao = client.post(
    "/livros",
    json={
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "ano": 2008
    })

    id_livro = response_criacao.json()["id"]

    response = client.put(
        f'/livros/{id_livro}',
        json={
            "titulo": "Clean Code - Atualizado",
            "autor": "Robert C. Martin",
            "ano": "ano"
        }
    )

    assert response.status_code==422

def testar_atualizar_livro_inexistente(client):

    response = client.put(
        "/livros/9999",
        json={
            "titulo": "Clean Code - Atualizado",
            "autor": "Robert C. Martin",
            "ano": 2000
        }
    )

    assert response.status_code==404

    assert response.json() == {
        "detail": "Livro não encontrado."
    }

def test_delete_livro(client):

    response_criacao = client.post("/livros",
                                   json={
                                        "titulo": "Clean Code",
                                        "autor": "Robert C. Martin",
                                        "ano": 2008
                                   })

    id_livro = response_criacao.json()["id"]

    response = client.delete(
        f'/livros/{id_livro}'
    )

    assert response.status_code==204

    response_busca = client.get(
        f"/livros/{id_livro}"
    )

    assert response_busca.status_code == 404

def testar_delete_livro_inexistente(client):
    response = client.delete("/livros/9999")

    assert response.status_code==404

    assert response.json() == {
        "detail": "Livro não encontrado"
    }
