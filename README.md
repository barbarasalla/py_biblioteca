# 📚 Biblioteca API

API REST para gerenciamento de livros, desenvolvida em Python com FastAPI.

O projeto foi construído como um projeto de estudo para praticar conceitos de desenvolvimento backend, arquitetura, persistência, APIs, testes, migrations e organização de código.


## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- Pydantic Settings
- Pytest
- Docker
- Docker Compose


## Funcionalidades

A API permite:

- Cadastrar livros
- Listar livros
- Buscar livro por ID
- Atualizar livros
- Excluir livros
- Cadastrar livro através de ISBN
- Persistir dados utilizando SQLite
- Carregar uma biblioteca inicial através de `biblioteca.json`
- Executar a aplicação em um container Docker
- Persistir o banco de dados utilizando Docker Volume


## Arquitetura

O projeto está organizado separando as principais responsabilidades:

```text
API / Router
     ↓
Service
     ↓
Repository
     ↓
SQLAlchemy
     ↓
SQLite
````

### Router

Responsável pela camada HTTP e pelos endpoints da API.

### Service

Contém as regras de negócio da aplicação.

### Repository

Responsável pelo acesso e persistência dos dados.

### Model

Representa as entidades persistidas no banco através do SQLAlchemy.

### Schema

Define os contratos de entrada e saída da API utilizando Pydantic.

### Dependencies

Centraliza a injeção de dependências utilizadas pela aplicação.

### Startup

Contém operações executadas durante a inicialização da aplicação, como a carga inicial da biblioteca.


## Estrutura do projeto

```text
py_biblioteca/
│
├── README.md
├── .env.example
├── .env.docker
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── biblioteca.json
│
├── alembic/
│   ├── README.md
│   ├── env.py
│   └── versions/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
|   |
│   ├── apis/
│   │   └── buscar_livro_api.py
│   │
│   ├── database/
│   │   └── database.py
|   |
│   ├── exceptions/
│   │   └── api_exceptions.py
│   │
│   ├── models/
│   │   └── livro.py
│   │
│   ├── schemas/
│   │   └── livro.py
│   │
│   ├── repositories/
│   │   └── livro_repository.py
│   │
│   ├── services/
│   │   └── livro_service.py
│   │
│   ├── routers/
│   │   └── livros.py
│   │
│   └── startup/
│       └── biblioteca_carga_inicial.py
│
└── tests/
    ├── conftest.py
    ├── test_api.py
    ├── test_livro.py
    ├── test_livro_repository.py
    └── test_livro_service.py
```


## Configuração

As configurações da aplicação são obtidas através de variáveis de ambiente utilizando Pydantic Settings.

- ### Desenvolvimento local

Crie um arquivo .env baseado no .env.example.

#### `.env`
```env
DATABASE_URL=sqlite:///biblioteca.db
BIBLIOTECA_JSON=biblioteca.json
```

O arquivo `.env` não deve ser versionado.

### Docker

Para execução através do Docker Compose, é utilizado o arquivo .env.docker:

#### `.env.docker`
```env
DATABASE_URL=sqlite:///data/biblioteca.db
BIBLIOTECA_JSON=biblioteca.json
```

O banco é armazenado em `/app/data` dentro do container e persistido através de um Docker Volume.

## Instalação

Se estiver utilizando `uv`:

```bash
uv sync
```

Ou instale as dependências utilizando o arquivo `requirements.txt` que contém as dependências da aplicação declaradas.

As dependências utilizadas durante o desenvolvimento e execução dos testes estão em:
`requirements-dev.txt`

Para instalar as dependências de desenvolvimento:
```bash
pip install -r requirements-dev.txt
```


## Banco de dados

O projeto utiliza SQLite para persistência.

Na execução local:
```text
biblioteca.db
```
No Docker:
```text
/app/data/biblioteca.db
```
O arquivo do banco é local e não é versionado no Git.

A estrutura do banco é controlada pelo Alembic.


## Migrations

O projeto utiliza Alembic para versionamento e evolução do schema do banco.

Para criar o banco a partir das migrations:

```bash
py -m alembic upgrade head
```

Criar uma migration automaticamente a partir de alterações nos Models:

```bash
py -m alembic revision --autogenerate -m "descrição da alteração"
```

Verificar a versão atual:

```bash
py -m alembic current
```

Ver o histórico:

```bash
py -m alembic history
```

Executar rollback:

```bash
py -m alembic downgrade <revision>
```

Para mais detalhes sobre Alembic e as migrations deste projeto, consulte:

```text
alembic/README.md
```

## Carga inicial

Ao iniciar a aplicação, a biblioteca pode ser carregada a partir de:

```text
biblioteca.json
```

A carga inicial ocorre somente quando não existem livros no banco.

O fluxo é:

```text
FastAPI
   ↓
lifespan
   ↓
BibliotecaCargaInicial
   ↓
biblioteca.json
   ↓
Repository
   ↓
SQLite
```
Quando executada através do Docker, a aplicação primeiro executa as migrations do Alembic e depois inicia o FastAPI.

## Executando a aplicação localmente

Execute:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```text
http://localhost:8000
```

A documentação interativa do FastAPI pode ser acessada em:

```text
http://localhost:8000/docs
```

## Testes

Os testes são executados com Pytest:

```bash
pytest
```

O projeto possui testes para diferentes camadas:

* Unitários
* Repository
* Service
* API / integração

Para executar com mais detalhes:

```bash
pytest -v
```

## Docker

A aplicação pode ser executada em um container Docker.

O `Dockerfile` define como a imagem da aplicação é construída.

O `docker-compose.yml` define a execução da aplicação, incluindo:

* Container da API
* Variáveis de ambiente
* Mapeamento de portas
* Docker Volume para persistência do banco

### Construir e executar

Para iniciar a aplicação utilizando Docker Compose:

```bash
docker compose up
```

O Compose constrói a imagem automaticamente quando necessário.

Para forçar a reconstrução da imagem:

```bash
docker compose up --build
```

A API estará disponível em:

```text
http://localhost:8000
```

A documentação:

```text
http://localhost:8000/docs
```

### Verificar os containers

```bash
docker compose ps
```

### Visualizar os logs

```bash
docker compose logs
```

Para acompanhar os logs em tempo real:

```bash
docker compose logs -f
```

### Parar a aplicação

```bash
docker compose down
```

O comando remove o container, mas mantém o volume e os dados do banco.

Para remover também os volumes:

```bash
docker compose down -v
```

> O comando `docker compose down -v` remove o volume utilizado pelo banco e, consequentemente, os dados persistidos.

## Docker Volume

O banco SQLite não é armazenado diretamente no filesystem temporário do container.

O Docker Compose utiliza o volume:

```text
biblioteca-data
```

montado em:

```text
/app/data
```

O fluxo é:

```text
Container
    │
    └── /app/data
            │
            ↓
      Docker Volume
            │
            ↓
     biblioteca.db
```

Dessa forma, o container pode ser removido e recriado sem perder os dados armazenados no volume.

## Fluxo de inicialização com Docker

Quando o container é iniciado:

```text
Docker Compose
      ↓
Container
      ↓
entrypoint.sh
      ↓
Alembic
      ↓
alembic upgrade head
      ↓
Banco atualizado
      ↓
Uvicorn
      ↓
FastAPI
      ↓
Carga inicial da biblioteca
```

As migrations são executadas antes da inicialização da API para garantir que o banco esteja com o schema atualizado.

## Fluxo para configurar o projeto do zero

### Execução local

Depois de clonar o projeto:

```bash
git clone <repository>
cd py_biblioteca
```

Crie o `.env` baseado no `.env.example`.

Instale as dependências:

```bash
py -m pip install -r requirements-dev.txt
```

Execute as migrations:

```bash
py -m alembic upgrade head
```

Execute os testes:

```bash
pytest
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

### Execução com Docker

Depois de clonar o projeto:

```bash
git clone <repository>
cd py_biblioteca
```

Configure o `.env.docker`.

Inicie a aplicação:

```bash
docker compose up
```

O Docker Compose irá:

1. Construir a imagem da aplicação.
2. Criar o container.
3. Criar ou utilizar o Docker Volume.
4. Executar as migrations do Alembic.
5. Iniciar a API.

## Documentação específica

### `README.md`

Documentação geral do projeto:

* Arquitetura
* Configuração
* Instalação
* Banco de dados
* Testes
* Docker
* Docker Compose

### `alembic/README.md`

Documentação específica sobre:

* Alembic
* Migrations
* `upgrade`
* `downgrade`
* `revision`
* `autogenerate`
* `current`
* `history`

## Próximos passos

O projeto está sendo evoluído gradualmente para praticar conceitos de desenvolvimento backend.

Próximas etapas:

* PostgreSQL
* Evolução da infraestrutura da aplicação