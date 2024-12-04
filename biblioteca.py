import pymongo
from pymongo import MongoClient
from livro import Livro
from usuario import Usuario

class Biblioteca:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["biblioteca"]
        self.livros = self.db["livros"]
        self.usuarios = self.db["usuarios"]

    def adicionar_livro(self, livro):
        self.livros.insert_one(livro.to_dict())
        print("Livro adicionado com sucesso!")

    def listar_livros(self):
        for livro in self.livros.find():
            print(f"Título: {livro['titulo']}, Autor: {livro['autor']}, ISBN: {livro['isbn']}")

    def atualizar_livro(self, isbn, novo_titulo):
        result = self.livros.update_one({"isbn": isbn}, {"$set": {"titulo": novo_titulo}})
        if result.matched_count > 0:
            print("Livro atualizado com sucesso!")
        else:
            print("Livro não encontrado.")

    def remover_livro(self, isbn):
        result = self.livros.delete_one({"isbn": isbn})
        if result.deleted_count > 0:
            print("Livro removido com sucesso!")
        else:
            print("Livro não encontrado.")
