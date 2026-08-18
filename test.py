from database import engine, Base, SessionLocal
from livro import Livro


Base.metadata.create_all(engine)
session = SessionLocal()

print("Tabelas criadas!")
livro = session.get(Livro, 1)

# livro = Livro(
#     titulo="Clean Code",
#     autor="Robert C. Martin",
#     ano=2008
# )

# session.add(livro)

session.commit()

print(livro.id)



session.close()