import requests

from api_exceptions import LivroNaoEncontradoError, APIConsumeError, LivroDadosInvalidosError


def fazer_requisicao(url):

    try:
        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as error:
        print(f"Erro HTTP: {response.status_code}")
        if response.status_code==404:
            raise LivroNaoEncontradoError(
                "Livro não encontrado na OpenLibrary."
            ) from error

        raise APIConsumeError(
            f"Erro HTTP ao consultar a OpenLibrary: {response.status_code}"
        ) from error

    except requests.exceptions.Timeout as error:
        print("A API OpenLibrary demorou muito para responder.")
        raise APIConsumeError(
            "A API OpenLibrary demorou muito para responder."
        ) from error

    except requests.exceptions.ConnectionError as error:
        print("Não foi possível conectar à API.")
        raise APIConsumeError(
            "Não foi possível conectar à OpenLibrary."
        ) from error

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")
        raise APIConsumeError(
            f"Erro na comunicação com a OpenLibrary: {erro}"
        ) from error

    except ValueError as error:
        print("A API retornou uma resposta que não é um JSON válido.")
        raise APIConsumeError(
            "A API retornou uma resposta que não é um JSON válido."
        ) from error

def buscar_livro_por_isbn(isbn):

    # Buscar informações do livro
    url_livro = f"https://openlibrary.org/isbn/{isbn}.json"

    dados_livro = fazer_requisicao(url_livro)

    if dados_livro is None:
        return None

    # Buscar detalhes da obra
    obras = dados_livro.get("works")

    if not obras:
        raise LivroDadosInvalidosError(
            "Não foi possível identificar informações sobre a obra."
        )

    chave_obra = obras[0].get("key")

    if not chave_obra:
        raise LivroDadosInvalidosError(
            "Não foi possível identificar informações sobre a obra."
        )

    url_obra = f"https://openlibrary.org{chave_obra}.json"

    dados_obra = fazer_requisicao(url_obra)

    if dados_obra is None:
        raise LivroDadosInvalidosError(
            "Não foi possível identificar informações sobre a obra."
        )

    # Buscar o autor
    autores = dados_obra.get("authors")

    if not autores:
        return None

    chave_autor = autores[0].get("author", {}).get("key")

    if not chave_autor:
        raise LivroDadosInvalidosError(
            "Não foi possível identificar o autor do livro."
        )

    url_autor = f"https://openlibrary.org{chave_autor}.json"

    dados_autor = fazer_requisicao(url_autor)

    if dados_autor is None:
        raise LivroDadosInvalidosError(
            "Não foi possível identificar o autor do livro."
        )

    # Montar resultado
    titulo = dados_livro.get("title")
    autor = dados_autor.get("name")

    publish_date = dados_livro.get("publish_date")

    if not publish_date:
        raise LivroDadosInvalidosError(
            "Não foi possível encontrar dados de data de publicação."
        )

    # Exemplo: "March 2008" -> 2008
    partes_data = publish_date.split()

    try:
        ano = next(
            int(parte)
            for parte in partes_data
            if parte.isdigit() and len(parte) == 4
        )
    except StopIteration:
        raise LivroDadosInvalidosError(
            "Não foi possível encontrar dados de data de publicação."
        )

    return {
        "titulo": titulo,
        "autor": autor,
        "ano": ano
    }