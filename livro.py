class Livro:

    def __init__(self, id, titulo, autor, ano):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

    def exibir(self):
        print(
            f"ID: {self.id} | "
            f"Título: {self.titulo} | "
            f"Autor: {self.autor} | "
            f"Ano: {self.ano}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["id"],
            dados["titulo"],
            dados["autor"],
            dados["ano"]
        )
