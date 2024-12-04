from tkinter import *
from tkinter import messagebox, simpledialog
from biblioteca import Biblioteca
from livro import Livro
from usuario import Usuario

class BibliotecaApp:
    def __init__(self, root):
        self.biblioteca = Biblioteca()
        self.root = root
        self.root.title("Biblioteca")

        # Exibir o menu principal assim que a aplicação iniciar
        self.menu_principal()

    def menu_principal(self):
        self.menu_frame = Frame(self.root)
        self.menu_frame.pack()

        Label(self.menu_frame, text="Bem-vindo à Biblioteca!").grid(row=0, columnspan=2)

        Button(self.menu_frame, text="Login Usuário", command=self.login_usuario).grid(row=1, column=0, pady=10)
        Button(self.menu_frame, text="Criar Usuário", command=self.criar_usuario).grid(row=1, column=1, pady=10)
        Button(self.menu_frame, text="Sair", command=self.root.quit).grid(row=2, column=0, columnspan=2, pady=10)

    def login_usuario(self):
        self.menu_frame.destroy()

        login_window = Toplevel(self.root)
        login_window.title("Login Usuário")

        Label(login_window, text="Nome do Usuário:").grid(row=0, column=0)
        usuario_nome_entry = Entry(login_window)
        usuario_nome_entry.grid(row=0, column=1)

        def entrar():
            usuario_nome = usuario_nome_entry.get()

            # Verificar se o usuário tem alguma devolução pendente
            emprestimos_pendentes = self.biblioteca.listar_emprestimos_do_usuario(usuario_nome)
            if emprestimos_pendentes != "Nenhum livro emprestado no momento.":
                devolver = messagebox.askyesno("Empréstimos Pendentes", f"Você tem os seguintes empréstimos pendentes:\n{emprestimos_pendentes}\nDeseja devolver algum?")
                if devolver:
                    isbn_para_devolver = simpledialog.askstring("Devolver Livro", "Digite o ISBN do livro que deseja devolver:")
                    if isbn_para_devolver:
                        self.biblioteca.devolver_livro(usuario_nome, isbn_para_devolver)

            # Depois do login, mostrar as opções do menu do usuário
            login_window.destroy()
            self.menu_usuario(usuario_nome)

        Button(login_window, text="Entrar", command=entrar).grid(row=1, column=0, columnspan=2, pady=10)

    def criar_usuario(self):
        criar_usuario_window = Toplevel(self.root)
        criar_usuario_window.title("Criar Usuário")

        Label(criar_usuario_window, text="Nome do Usuário:").grid(row=0, column=0)
        nome_entry = Entry(criar_usuario_window)
        nome_entry.grid(row=0, column=1)

        Label(criar_usuario_window, text="Idade do Usuário:").grid(row=1, column=0)
        idade_entry = Entry(criar_usuario_window)
        idade_entry.grid(row=1, column=1)

        Label(criar_usuario_window, text="Email do Usuário:").grid(row=2, column=0)
        email_entry = Entry(criar_usuario_window)
        email_entry.grid(row=2, column=1)

        def criar():
            nome = nome_entry.get()
            idade = int(idade_entry.get())
            email = email_entry.get()
            usuario = Usuario(nome, idade, email)
            self.biblioteca.adicionar_usuario(usuario)
            criar_usuario_window.destroy()
            messagebox.showinfo("Usuário Criado", "Usuário criado com sucesso!")

        Button(criar_usuario_window, text="Criar", command=criar).grid(row=3, column=0, columnspan=2, pady=10)

    def menu_usuario(self, usuario_nome):
        self.usuario_menu_frame = Frame(self.root)
        self.usuario_menu_frame.pack()

        Label(self.usuario_menu_frame, text=f"Bem-vindo, {usuario_nome}!").grid(row=0, columnspan=2)

        Button(self.usuario_menu_frame, text="Listar Todos os Livros", command=self.listar_livros).grid(row=1, column=0, pady=5)
        Button(self.usuario_menu_frame, text="Listar Livros Emprestados", command=lambda: self.listar_livros_usuario(usuario_nome)).grid(row=1, column=1, pady=5)
        Button(self.usuario_menu_frame, text="Adicionar Livro", command=self.adicionar_livro).grid(row=2, column=0, pady=5)
        Button(self.usuario_menu_frame, text="Remover Livro", command=self.remover_livro).grid(row=2, column=1, pady=5)
        Button(self.usuario_menu_frame, text="Pegar Livro", command=lambda: self.pegar_livro(usuario_nome)).grid(row=3, column=0, pady=5)
        Button(self.usuario_menu_frame, text="Devolver Livro", command=lambda: self.devolver_livro(usuario_nome)).grid(row=3, column=1, pady=5)
        Button(self.usuario_menu_frame, text="Sair", command=self.voltar_para_menu_principal).grid(row=4, column=0, columnspan=2, pady=10)

    def voltar_para_menu_principal(self):
        self.usuario_menu_frame.destroy()
        self.menu_principal()

    def listar_livros(self):
        livros = self.biblioteca.listar_livros()
        messagebox.showinfo("Livros na Biblioteca", livros)

    def listar_livros_usuario(self, usuario_nome):
        livros = self.biblioteca.listar_livros_usuario(usuario_nome)
        messagebox.showinfo(f"Livros Emprestados por {usuario_nome}", livros)

    def adicionar_livro(self):
        adicionar_livro_window = Toplevel(self.root)
        adicionar_livro_window.title("Adicionar Livro")

        Label(adicionar_livro_window, text="Título do Livro:").grid(row=0, column=0)
        titulo_entry = Entry(adicionar_livro_window)
        titulo_entry.grid(row=0, column=1)

        Label(adicionar_livro_window, text="Autor do Livro:").grid(row=1, column=0)
        autor_entry = Entry(adicionar_livro_window)
        autor_entry.grid(row=1, column=1)

        Label(adicionar_livro_window, text="ISBN do Livro:").grid(row=2, column=0)
        isbn_entry = Entry(adicionar_livro_window)
        isbn_entry.grid(row=2, column=1)

        def adicionar():
            titulo = titulo_entry.get()
            autor = autor_entry.get()
            isbn = isbn_entry.get()
            livro = Livro(titulo, autor, isbn)
            self.biblioteca.adicionar_livro(livro)
            adicionar_livro_window.destroy()
            messagebox.showinfo("Livro Adicionado", "Livro adicionado com sucesso!")

        Button(adicionar_livro_window, text="Adicionar", command=adicionar).grid(row=3, column=0, columnspan=2, pady=10)

    def remover_livro(self):
        remover_livro_window = Toplevel(self.root)
        remover_livro_window.title("Remover Livro")

        Label(remover_livro_window, text="ISBN do Livro:").grid(row=0, column=0)
        isbn_entry = Entry(remover_livro_window)
        isbn_entry.grid(row=0, column=1)

        def remover():
            isbn = isbn_entry.get()
            self.biblioteca.remover_livro(isbn)
            remover_livro_window.destroy()
            messagebox.showinfo("Livro Removido", "Livro removido com sucesso!")

        Button(remover_livro_window, text="Remover", command=remover).grid(row=1, column=0, columnspan=2, pady=10)

    def pegar_livro(self, usuario_nome):
        pegar_livro_window = Toplevel(self.root)
        pegar_livro_window.title("Pegar Livro")

        Label(pegar_livro_window, text="ISBN do Livro:").grid(row=0, column=0)
        isbn_entry = Entry(pegar_livro_window)
        isbn_entry.grid(row=0, column=1)

        def pegar():
            isbn = isbn_entry.get()
            self.biblioteca.pegar_livro(usuario_nome, isbn)
            pegar_livro_window.destroy()

        Button(pegar_livro_window, text="Pegar Livro", command=pegar).grid(row=1, column=0, columnspan=2, pady=10)

    def devolver_livro(self, usuario_nome):
        devolver_livro_window = Toplevel(self.root)
        devolver_livro_window.title("Devolver Livro")

        Label(devolver_livro_window, text="ISBN do Livro:").grid(row=0, column=0)
        isbn_entry = Entry(devolver_livro_window)
        isbn_entry.grid(row=0, column=1)

        def devolver():
            isbn = isbn_entry.get()
            self.biblioteca.devolver_livro(usuario_nome, isbn)
            devolver_livro_window.destroy()

        Button(devolver_livro_window, text="Devolver Livro", command=devolver).grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = Tk()
    app = BibliotecaApp(root)
    root.mainloop()
