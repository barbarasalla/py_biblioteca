import requests


def fazer_requisicao(url):

    try:
        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError:
        print(f"Erro HTTP: {response.status_code}")
        return None

    except requests.exceptions.Timeout:
        print("A API demorou muito para responder.")
        return None

    except requests.exceptions.ConnectionError:
        print("Não foi possível conectar à API.")
        return None

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")
        return None

    except ValueError:
        print("A API retornou uma resposta que não é um JSON válido.")
        return None


def buscar_livro_por_isbn(isbn):

    # Buscar informações do livro
    url_livro = f"https://openlibrary.org/isbn/{isbn}.json"

    dados_livro = fazer_requisicao(url_livro)

    if dados_livro is None:
        return None

    # Buscar detalhes da obra
    obras = dados_livro.get("works")

    if not obras:
        return None

    chave_obra = obras[0].get("key")

    if not chave_obra:
        return None

    url_obra = f"https://openlibrary.org{chave_obra}.json"

    dados_obra = fazer_requisicao(url_obra)

    if dados_obra is None:
        return None

    # Buscar o autor
    autores = dados_obra.get("authors")

    if not autores:
        return None

    chave_autor = autores[0].get("author", {}).get("key")

    if not chave_autor:
        return None

    url_autor = f"https://openlibrary.org{chave_autor}.json"

    dados_autor = fazer_requisicao(url_autor)

    if dados_autor is None:
        return None

    # Montar resultado
    titulo = dados_livro.get("title")
    autor = dados_autor.get("name")

    publish_date = dados_livro.get("publish_date")

    if not publish_date:
        return None

    # Exemplo: "March 2008" -> 2008
    partes_data = publish_date.split()

    try:
        ano = next(
            int(parte)
            for parte in partes_data
            if parte.isdigit() and len(parte) == 4
        )
    except StopIteration:
        return None

    return {
        "titulo": titulo,
        "autor": autor,
        "ano": ano
    }