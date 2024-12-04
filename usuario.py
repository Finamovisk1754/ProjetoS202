class Usuario:
    def __init__(self, nome, idade, email):
        self.nome = nome
        self.idade = idade
        self.email = email

    def to_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "email": self.email
        }
