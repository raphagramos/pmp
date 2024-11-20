from tkinter import *
from connections import conectar_banco
from Pages.MainFile import main
import bcrypt  # Para segurança das senhas


class LoginScreen:
    def __init__(self, master=None):
        self.master = master
        self.fontePadrao = ("Arial", "10")

        # Conexão ao banco
        self.mydb, self.cursor = conectar_banco()
        if not self.mydb or not self.cursor:
            print("Erro ao conectar ao banco de dados.")
            return

        # Containers
        self.primeiroContainer = Frame(self.master, pady=10)
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(self.master, padx=20)
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(self.master, padx=20)
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(self.master, pady=20)
        self.quartoContainer.pack()

        # Versão
        self.versao = Label(self.master, text="Versão 0.0.1", font=("Arial", 8))
        self.versao.pack(side=BOTTOM)

        # Título
        self.titulo = Label(self.primeiroContainer, text="Dados do usuário", font=("Arial", 10, "bold"))
        self.titulo.pack()

        # Lista de usuários
        self.cursor.execute("SELECT usuario FROM usuarios")
        lov_users = [user[0] for user in self.cursor.fetchall()]
        self.clicked = StringVar(value=lov_users[0] if lov_users else "Nenhum usuário encontrado")
        self.nomeLabel = OptionMenu(self.master, self.clicked, *lov_users)
        self.nomeLabel.pack(side=TOP)

        # Campo para senha
        self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
        self.senhaLabel.pack(side=TOP)
        self.senha = Entry(self.terceiroContainer, width=30, font=self.fontePadrao, show="*")
        self.senha.pack(side=TOP)

        # Botão autenticar
        self.autenticar = Button(self.quartoContainer, text="Autenticar", font=("Calibri", 8), width=12, command=self.verificaSenha)
        self.autenticar.pack()

        # Mensagem de erro/sucesso
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def verificaSenha(self):
        usuario = self.clicked.get()  # Obtém o usuário selecionado no OptionMenu
        senha = self.senha.get()

        if not usuario or not senha:
            self.mensagem["text"] = "Preencha todos os campos."
            return

        # Consulta para buscar o hash da senha
        query = "SELECT senha FROM usuarios WHERE usuario = %s"
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchone()

        if resultado:
            senha_armazenada = resultado[0]  # A senha armazenada é um hash
            if bcrypt.checkpw(senha.encode(), senha_armazenada.encode()):
                self.master.destroy()  # Fecha a janela de login
                self.main_window = main()  # Criação de uma instância da janela principal
                self.main_window.master.mainloop()  # A instância master dentro de main()
            else:
                self.mensagem["text"] = "Senha incorreta."
        else:
            self.mensagem["text"] = "Usuário não encontrado."

    def __del__(self):
        # Fechar conexão ao banco
        if self.cursor:
            self.cursor.close()
        if self.mydb:
            self.mydb.close()
