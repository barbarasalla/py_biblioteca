# Alembic

## O que é o Alembic?

Alembic é uma ferramenta de **migrations para bancos de dados**, utilizada principalmente com SQLAlchemy.

Uma migration representa uma alteração na estrutura do banco e permite controlar a evolução do schema ao longo do tempo.

Exemplo:

```text
Banco v1
   ↓ migration
Banco v2
   ↓ migration
Banco v3
````

Isso permite que diferentes ambientes mantenham o banco na mesma versão.

---

## Por que utilizar?

O SQLAlchemy permite definir o modelo do banco através dos Models:

```python
class Livro(Base):
    ...
```

Porém, o Model representa o **estado atual desejado** do banco. Ele não mantém o histórico das alterações.

O Alembic mantém esse histórico através das migrations.

Exemplo:

```text
Model atual
    ↓
Alembic detecta alterações
    ↓
Migration
    ↓
Banco atualizado
```

As migrations são versionadas junto com o código e podem ser executadas em outros ambientes.

---

# Instalação

Com `uv`:

```bash
uv add --dev alembic
```

Ou com `pip`:

```bash
pip install alembic
```

Verificar a instalação:

```bash
alembic --version
```

No projeto também pode ser utilizado:

```bash
py -m alembic --version
```

---

# Inicialização

```bash
alembic init alembic
```

Esse comando gera a estrutura inicial:

- alembic.ini           → Configuração do Alembic.
- alembic/              → Pasta que contém a estrutura das migrations.
- - alembic/versions/   → Local onde as migrations são armazenadas.
- - alembic/env.py      → Arquivo Python responsável por configurar como o Alembic acessa a aplicação e executa as migrations.

---
# Como o Alembic funciona no projeto

O projeto utiliza SQLAlchemy para definir os Models.

O `Livro` herda de:

```python
class Livro(Base):
```

O `Base` mantém o metadata dos Models:

```python
Base.metadata
```

No `alembic/env.py` configuramos:

```python
target_metadata = Base.metadata
```

Isso permite ao Alembic comparar o estado definido pelos Models com o schema atual do banco.

---

# Configuração do banco

O projeto utiliza `pydantic-settings` para centralizar as configurações.

`.env`:

```env
DATABASE_URL=sqlite:///biblioteca.db
BIBLIOTECA_JSON=biblioteca.json
```

`app/config.py` disponibiliza:

```python
settings.database_url
```

O SQLAlchemy utiliza essa configuração para criar o Engine.

O Alembic também utiliza:

```python
settings.database_url
```

Assim existe uma única configuração da URL do banco.

Não é necessário manter uma segunda URL diferente no `alembic.ini`.

---

# Configuração do env.py

O `alembic/env.py` importa o `Base` e o `Engine` da aplicação:

```python
from app.database.database import Base, engine
```

Também importa os Models que devem estar registrados no metadata:

```python
from app.models.livro import Livro
```

E define:

```python
target_metadata = Base.metadata
```

O Alembic utiliza esse metadata para o `--autogenerate`.

O `env.py` possui dois modos:

```text
offline
online
```

### Offline

Executa/configura migrations sem utilizar uma conexão persistente com o banco.

Utiliza:

```python
settings.database_url
```

### Online

Utiliza o Engine da aplicação:

```python
with engine.connect() as connection:
```

e executa as migrations através dessa conexão.

---

# Migration

Uma migration possui principalmente:

```python
def upgrade():
    ...
```

e:

```python
def downgrade():
    ...
```

### upgrade

Avança o schema do banco.

Exemplo:

```python
op.add_column(
    "livros",
    sa.Column(
        "isbn",
        sa.String(length=13),
        nullable=True
    )
)
```

### downgrade

Desfaz a alteração realizada pelo `upgrade`.

Exemplo:

```python
op.drop_column(
    "livros",
    "isbn"
)
```

---

# Migration inicial do projeto

O banco `biblioteca.db` já existia localmente e não é versionado no Git.

Por isso foi criada uma migration inicial que representa a criação da tabela:

```text
8a213f19566c_create_livros_table.py
```

Ela cria:

```text
livros
├── id
├── titulo
├── autor
└── ano
```

A migration possui:

```python
upgrade()
```

para criar a tabela e:

```python
downgrade()
```

para removê-la.

---

# Banco existente x banco novo

Essa diferença é importante.

## Banco novo

Quando `biblioteca.db` ainda não existe:

```bash
alembic upgrade head
```

executa as migrations necessárias e cria a estrutura do banco.

Isso permite que outra pessoa clone o projeto sem precisar receber o arquivo `biblioteca.db`.

---

## Banco existente

Quando o banco já possui a estrutura correspondente à migration, não devemos executar novamente o `upgrade` inicial.

Utilizamos:

```bash
alembic stamp head
```

O `stamp` **não executa a migration**.

Ele apenas informa ao Alembic que o banco já está naquela versão.

O Alembic registra essa informação na tabela:

```text
alembic_version
```

---

# Autogenerate

O comando:

```bash
alembic revision --autogenerate -m "mensagem"
```

compara:

```text
Base.metadata
     ↓
Models atuais
```

com:

```text
schema atual do banco
```

e gera uma migration contendo as diferenças encontradas.

Importante:

> `--autogenerate` gera uma sugestão de migration. A migration deve ser revisada antes de ser aplicada.

---

# Exemplo realizado no projeto

Foi adicionado `isbn` ao Model `Livro`:

```python
isbn: Mapped[str | None] = mapped_column(
    String(13),
    nullable=True
)
```

Depois foi executado:

```bash
alembic revision --autogenerate -m "add isbn to livros"
```

O Alembic identificou a nova coluna e gerou:

```python
op.add_column(
    "livros",
    sa.Column(
        "isbn",
        sa.String(length=13),
        nullable=True
    )
)
```

E no `downgrade`:

```python
op.drop_column(
    "livros",
    "isbn"
)
```

Depois a migration foi aplicada com:

```bash
alembic upgrade head
```

---

# Principais comandos

## Criar uma migration

```bash
alembic revision -m "mensagem"
```

Cria uma migration vazia para edição manual.

---

## Criar migration automaticamente

```bash
alembic revision --autogenerate -m "mensagem"
```

Compara o `Base.metadata` com o banco e gera as alterações detectadas.

Sempre revisar a migration gerada antes de aplicá-la.

---

## Aplicar migrations

```bash
alembic upgrade head
```

Leva o banco até a última migration existente.

---

## Aplicar uma migration específica

```bash
alembic upgrade <revision>
```

Executa migrations até a revision informada.

---

## Voltar uma migration

```bash
alembic downgrade <revision>
```

Desfaz migrations até chegar à revision informada.

Exemplo utilizado no projeto:

```bash
alembic downgrade 8a213f19566c
```

---

## Voltar uma migration

Também é possível usar:

```bash
alembic downgrade -1
```

Isso volta uma migration a partir da versão atual.

---

## Ver a versão atual do banco

```bash
alembic current
```

Mostra qual migration está registrada como atual no banco.

---

## Ver histórico

```bash
alembic history
```

Mostra as migrations existentes no projeto e a relação entre elas.

Exemplo:

```text
8a213f19566c -> 6d65ad6de28c
<base> -> 8a213f19566c
```

`history` mostra o histórico disponível.

`current` mostra a versão atualmente registrada no banco.

---

## Verificar se existem alterações pendentes

```bash
alembic check
```

Verifica se existem alterações no metadata que ainda não possuem migration.

---

## Marcar uma versão sem executar a migration

```bash
alembic stamp head
```

Atualiza a versão registrada pelo Alembic sem executar as operações de `upgrade()`.

É útil quando um banco já existente corresponde ao estado de uma migration.

---

# Comandos utilizados para validar o projeto

Fluxo recomendado após alterar Models:

```bash
# 1. Gerar migration
alembic revision --autogenerate -m "descrição"

# 2. Revisar o arquivo gerado

# 3. Aplicar migration
alembic upgrade head

# 4. Verificar versão atual
alembic current

# 5. Executar testes
pytest
```

Para testar rollback:

```bash
alembic downgrade <revision>
```

Depois:

```bash
alembic current
```

E para retornar à versão mais recente:

```bash
alembic upgrade head
```

---

# Alembic x SQLAlchemy

SQLAlchemy:

> Define os Models e fornece o acesso ao banco.

Alembic:

> Controla a evolução e o versionamento do schema do banco.

Resumo:

```text
SQLAlchemy
    ↓
Model / Base.metadata
    ↓
estado desejado


Alembic
    ↓
Migration
    ↓
alteração do schema


Banco
    ↓
estado atual
```

---

# Alembic x create_all()

No início do projeto era utilizado:

```python
Base.metadata.create_all(engine)
```

Esse recurso é útil para criar tabelas que ainda não existem, mas não é uma ferramenta de versionamento de schema.

Com Alembic:

```text
Model
  ↓
Migration
  ↓
Banco
```

A aplicação deixou de utilizar `create_all()` no startup.

O Alembic passou a ser responsável pela criação e evolução da estrutura do banco.

A carga dos dados iniciais continua sendo responsabilidade da aplicação:

```text
Alembic
    ↓
estrutura do banco

biblioteca.json
    ↓
dados iniciais
```

---

# Fluxo atual do projeto

Ao preparar um banco novo:

```bash
alembic upgrade head
```

Depois a aplicação pode ser iniciada:

```bash
uvicorn app.main:app --reload
```

Durante o startup:

```text
Alembic
    ↓
estrutura do banco

FastAPI
    ↓
lifespan
    ↓
BibliotecaCargaInicial
    ↓
biblioteca.json
    ↓
livros iniciais
```

---

# Regra prática

Sempre que alterar um Model que representa uma alteração no schema:

```text
1. Alterar Model
2. Gerar migration
3. Revisar migration
4. Aplicar migration
5. Executar testes
```

Comandos:

```bash
alembic revision --autogenerate -m "descrição"
alembic upgrade head
pytest
```

Nunca considerar o `--autogenerate` como substituto da revisão manual da migration.