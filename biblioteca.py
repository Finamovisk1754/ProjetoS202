import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta

class Biblioteca:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["biblioteca"]
        self.livros = self.db["livros"]
        self.usuarios = self.db["usuarios"]
        self.emprestimos = self.db["emprestimos"]

    def adicionar_livro(self, livro):
        self.livros.insert_one(livro.to_dict())
        print("Livro adicionado com sucesso!")

    def listar_livros(self):
        livros_str = ""
        for livro in self.livros.find():
            livros_str += f"Título: {livro['titulo']}, Autor: {livro['autor']}, ISBN: {livro['isbn']}\n"
        return livros_str if livros_str else "Nenhum livro encontrado."

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
        usuarios_str = ""
        for usuario in self.usuarios.find():
            usuarios_str += f"Nome: {usuario['nome']}, Idade: {usuario['idade']}, Email: {usuario['email']}, Admin: {usuario.get('is_admin', False)}\n"
        return usuarios_str if usuarios_str else "Nenhum usuário encontrado."

    def pegar_livro(self, usuario_nome, isbn):
        livro = self.livros.find_one({"isbn": isbn})
        if not livro:
            print("Livro não encontrado.")
            return

        emprestimo_existente = self.emprestimos.find_one({"isbn": isbn, "devolvido": False})
        if emprestimo_existente:
            print("Livro já está emprestado.")
            return

        usuario = self.usuarios.find_one({"nome": usuario_nome})
        if not usuario:
            print("Usuário não encontrado.")
            return

        data_emprestimo = datetime.now()
        data_devolucao = data_emprestimo + timedelta(days=7)

        emprestimo = {
            "isbn": isbn,
            "titulo": livro["titulo"],
            "autor": livro["autor"],
            "usuario_nome": usuario_nome,
            "data_emprestimo": data_emprestimo,
            "data_devolucao": data_devolucao,
            "devolvido": False
        }
        self.emprestimos.insert_one(emprestimo)

        # Remover o livro da coleção de livros disponíveis
        self.livros.delete_one({"isbn": isbn})

        print(f"Livro emprestado com sucesso! Prazo para devolução: {data_devolucao.strftime('%d/%m/%Y')}")

    def listar_emprestimos_do_usuario(self, usuario_nome):
        emprestimos = self.emprestimos.find({"usuario_nome": usuario_nome, "devolvido": False})
        emprestimos_str = ""
        for emprestimo in emprestimos:
            emprestimos_str += f"Título: {emprestimo['titulo']}, Autor: {emprestimo['autor']}, ISBN: {emprestimo['isbn']}, Data de Devolução: {emprestimo['data_devolucao'].strftime('%d/%m/%Y')}\n"
        return emprestimos_str if emprestimos_str else "Nenhum livro emprestado no momento."

    def devolver_livro(self, usuario_nome, isbn):
        emprestimo = self.emprestimos.find_one({"usuario_nome": usuario_nome, "isbn": isbn, "devolvido": False})
        if emprestimo:
            self.emprestimos.update_one({"_id": emprestimo["_id"]}, {"$set": {"devolvido": True}})
            # Adicionar o livro de volta à coleção de livros disponíveis
            livro = {
                "titulo": emprestimo["titulo"],
                "autor": emprestimo["autor"],
                "isbn": isbn
            }
            self.livros.insert_one(livro)
            print("Livro devolvido com sucesso!")
        else:
            print("Nenhum empréstimo ativo encontrado para este livro e usuário.")

    def listar_livros_usuario(self, usuario_nome):
        emprestimos = self.emprestimos.find({"usuario_nome": usuario_nome, "devolvido": False})
        livros_str = ""
        for emprestimo in emprestimos:
            livros_str += f"Título: {emprestimo['titulo']}, Autor: {emprestimo['autor']}, ISBN: {emprestimo['isbn']}\n"
        return livros_str if livros_str else "Nenhum livro emprestado no momento."
