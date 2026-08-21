#!/bin/sh

# Executa as migrations antes de iniciar a aplicação.
python -m alembic upgrade head

# Inicia a API.
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000