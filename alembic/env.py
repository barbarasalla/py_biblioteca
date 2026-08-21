from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database.database import Base, engine  # Importar o Base.metadata do projeto e tambpem o Engine ja configurado
from app.models.livro import Livro      # Importar o Model relacionado ao Base

from app.config import settings         # para o Alembic utilizar os dados das variaveis de ambiente existente do projeto.

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:     # Apenas mantém a configuração de logs do Alembic.
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata             # Metadata que o Alembic deve observar.

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """
    Executa migrations sem criar uma conexão persistente
    com o banco.

    Nesse modo o Alembic trabalha utilizando a URL
    do banco para gerar/executar o SQL necessário.
    """
    url = settings.database_url         # Utiliza a mesma configuração da aplicação
                                        # Dessa forma não precisamos duplicar a URL no alembic.ini.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,  # Faz com que valores sejam escritos diretamente no SQL gerado.
        dialect_opts={"paramstyle": "named"},  # Configuração específica para o dialeto utilizado.
    )

    with context.begin_transaction():   # Inicia uma transação para execução das migrations.
        context.run_migrations()        # Executa as migrations.


def run_migrations_online() -> None:
    """
    Executa migrations utilizando uma conexão real com o banco.
    """
    # Reutiliza o Engine configurado pela aplicação.
    # Isso evita criar outro Engine apenas para o Alembic.
    with engine.connect() as connection:

        # Configura o contexto do Alembic utilizando
        # a conexão aberta e o metadata dos Models.
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        # Inicia uma transação.
        with context.begin_transaction():

            # Executa as migrations.
            context.run_migrations()

# O Alembic pode executar migrations de duas maneiras:
    # offline → sem conexão persistente
    # online  → utilizando conexão com o banco
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
