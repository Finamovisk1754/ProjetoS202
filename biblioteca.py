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

    def adicionar_usuario(self, usuario):
        self.usuarios.insert_one(usuario.to_dict())
        print("Usuário adicionado com sucesso!")

    def listar_usuarios(self):
        for usuario in self.usuarios.find():
            print(f"Nome: {usuario['nome']}, Idade: {usuario['idade']}, Email: {usuario['email']}")

    def menu(self):
        while True:
            print("\n--- Menu Biblioteca ---")
            print("1. Adicionar Livro")
            print("2. Listar Livros")
            print("3. Atualizar Livro")
            print("4. Remover Livro")
            print("5. Adicionar Usuário")
            print("6. Listar Usuários")
            print("7. Sair")
            
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                titulo = input("Título do livro: ")
                autor = input("Autor do livro: ")
                isbn = input("ISBN do livro: ")
                livro = Livro(titulo, autor, isbn)
                self.adicionar_livro(livro)
            elif opcao == "2":
                self.listar_livros()
            elif opcao == "3":
                isbn = input("ISBN do livro a ser atualizado: ")
                novo_titulo = input("Novo título do livro: ")
                self.atualizar_livro(isbn, novo_titulo)
            elif opcao == "4":
                isbn = input("ISBN do livro a ser removido: ")
                self.remover_livro(isbn)
            elif opcao == "5":
                nome = input("Nome do usuário: ")
                idade = int(input("Idade do usuário: "))
                email = input("Email do usuário: ")
                usuario = Usuario(nome, idade, email)
                self.adicionar_usuario(usuario)
            elif opcao == "6":
                self.listar_usuarios()
            elif opcao == "7":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")
