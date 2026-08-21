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
├── .gitignore
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

As configurações da aplicação são obtidas através de variáveis de ambiente.

Crie um arquivo `.env` a partir do `.env.example`.

### `.env`

```env
DATABASE_URL=sqlite:///biblioteca.db
BIBLIOTECA_JSON=biblioteca.json
```

O arquivo `.env` não deve ser versionado.


## Instalação

Se estiver utilizando `uv`:

```bash
uv sync
```

Ou instale as dependências utilizando o método de gerenciamento de pacotes adotado no projeto.


## Banco de dados

O projeto utiliza SQLite para persistência:

```text
biblioteca.db
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

## Executando a aplicação

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

## Fluxo para configurar o projeto do zero

Depois de clonar o projeto:

```bash
git clone <repository>
cd py_biblioteca
```

Crie o `.env` baseado no `.env.example`.

Depois instale as dependências e execute as migrations:

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


## Próximos passos

O projeto está sendo evoluído gradualmente para praticar conceitos de desenvolvimento backend.

Próximas etapas:

* Containerização com Docker
* Docker Compose
* Persistência através de volumes
* PostgreSQL
* Evolução da infraestrutura da aplicação

### `README.md`

> **Como entender, instalar, executar e testar o projeto?**

### `alembic/README.md`

> **Como funciona o Alembic e como trabalhar com migrations?**