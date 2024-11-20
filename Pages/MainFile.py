import bcrypt
import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import messagebox
import threading

from connections import conectar_banco  # Para usar threads

class main:
    def __init__(self):
        self.master = Tk()  # Criação de uma instância da janela principal
        self.master.geometry("1280x720")  # Defina o tamanho da janela
        self.master.title("PMP - Pesagens Matéria Prima")
        
        # Criação da barra de menu
        self.menu_bar = Menu(self.master)

        # Menu Pesagens
        self.menu_pesagens = Menu(self.menu_bar, tearoff=0)
        self.menu_pesagens.add_command(label="Adicionar Pesagem")
        self.menu_pesagens.add_command(label="Consultar Pesagens")
        self.menu_bar.add_cascade(label="Pesagens", menu=self.menu_pesagens)

        # Menu Matéria Prima
        self.menu_mp = Menu(self.menu_bar, tearoff=0)
        self.menu_mp.add_command(label="Adicionar Matéria Prima")
        self.menu_mp.add_command(label="Consultar Matéria Prima")
        self.menu_bar.add_cascade(label="Matéria Prima", menu=self.menu_mp)

        # Menu Configurações
        self.menu_balanca = Menu(self.menu_bar, tearoff=0)
        self.menu_balanca.add_command(label="Cadastro de Usuários", command=self.abrir_tela_cadastro_usuario)
        self.menu_balanca.add_command(label="Configurar Balança", command=self.abrir_config_balanca)
        self.menu_bar.add_cascade(label="Configurações", menu=self.menu_balanca)

        # Adicionar a barra de menus à janela
        self.master.config(menu=self.menu_bar)

        # Exemplo de conteúdo principal
        label = Label(self.master, text="Bem-vindo à tela principal!", font=("Arial", 24))
        label.pack(pady=20)

        # Rodar o loop de eventos da janela principal
        self.master.mainloop()
    
    def abrir_tela_cadastro_usuario(self):
        # Cria uma nova janela para o cadastro de usuário
        cadastro_window = Toplevel(self.master)  # Toplevel cria uma nova janela
        cadastro_window.title("Cadastro de Usuário")
        cadastro_window.geometry("400x300")

        # Labels e campos de entrada para nome de usuário e senha
        label_usuario = Label(cadastro_window, text="Nome de Usuário:")
        label_usuario.pack(pady=10)

        entry_usuario = Entry(cadastro_window, width=30)
        entry_usuario.pack(pady=5)

        label_senha = Label(cadastro_window, text="Senha:")
        label_senha.pack(pady=10)

        entry_senha = Entry(cadastro_window, width=30, show="*")
        entry_senha.pack(pady=5)

        # Função para salvar o novo usuário no banco de dados
        def salvar_usuario():
            usuario = entry_usuario.get()
            senha = entry_senha.get()

            if not usuario or not senha:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            # Gerar o hash da senha usando bcrypt
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

            # Conectar ao banco e inserir o novo usuário
            try:
                mydb, cursor = conectar_banco()
                if not mydb or not cursor:
                    messagebox.showerror("Erro de conexão", "Não foi possível conectar ao banco de dados.")
                    return

                query = "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)"
                cursor.execute(query, (usuario, senha_hash))
                mydb.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                cadastro_window.destroy()  # Fechar a janela de cadastro após o sucesso

                # Fechar a conexão com o banco
                cursor.close()
                mydb.close()

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        # Botão para salvar o novo usuário
        botao_salvar = Button(cadastro_window, text="Salvar", command=salvar_usuario)
        botao_salvar.pack(pady=20)

        # Botão para fechar a janela
        botao_fechar = Button(cadastro_window, text="Fechar", command=cadastro_window.destroy)
        botao_fechar.pack(pady=5)
    
    def abrir_config_balanca(self):
        # Cria uma nova janela para configurar a balança
        config_window = Toplevel(self.master)  # Toplevel cria uma nova janela
        config_window.title("Configuração da Balança")
        config_window.geometry("400x300")

        # Labels e campos de entrada para seleção da porta serial
        label_balanca = Label(config_window, text="Selecione a porta serial da balança:")
        label_balanca.pack(pady=10)

        # Listar as portas seriais disponíveis
        portas = self.listar_portas_seriais()
        porta_var = StringVar(value=portas[0] if portas else "Nenhuma porta encontrada")

        porta_dropdown = OptionMenu(config_window, porta_var, *portas)
        porta_dropdown.pack(pady=10)

        # Função para conectar e ler dados da balança (usando thread)
        def conectar_balanca():
            porta = porta_var.get()
            if porta == "Nenhuma porta encontrada":
                messagebox.showwarning("Erro", "Nenhuma porta serial disponível.")
                return

            # Iniciar uma thread para conectar à balança e ler os dados
            threading.Thread(target=self.ler_dados_balanca, args=(porta,), daemon=True).start()

        # Função para testar a pesagem
        def testar_pesagem():
            porta = porta_var.get()
            if porta == "Nenhuma porta encontrada":
                messagebox.showwarning("Erro", "Nenhuma porta serial disponível.")
                return
            
            # Conectar à balança e ler um valor de teste
            threading.Thread(target=self.ler_dados_balanca, args=(porta,), daemon=True).start()

        # Botão para conectar à balança e ler dados
        botao_conectar = Button(config_window, text="Conectar à Balança", command=conectar_balanca)
        botao_conectar.pack(pady=10)

        # Botão para testar a pesagem
        botao_testar_pesagem = Button(config_window, text="Testar Pesagem", command=testar_pesagem)
        botao_testar_pesagem.pack(pady=10)

        # Botão para fechar a janela
        botao_fechar = Button(config_window, text="Fechar", command=config_window.destroy)
        botao_fechar.pack(pady=5)

    def listar_portas_seriais(self):
        # Função para listar as portas seriais disponíveis
        portas = [port.device for port in serial.tools.list_ports.comports()]
        if not portas:
            portas.append("Nenhuma porta encontrada")
        return portas

    def ler_dados_balanca(self, porta):
        try:
            # Abrir a porta serial
            ser = serial.Serial(porta, 9600, timeout=1)  # Ajuste conforme necessário
            ser.flush()  # Limpar buffers de entrada e saída

            # Loop contínuo para ler os dados da balança
            while ser.is_open:
                if ser.in_waiting > 0:  # Verificar se há dados disponíveis
                    leitura = ser.readline().decode('ascii').strip()
                    if leitura:
                        # Atualizar a interface com o valor lido
                        self.master.after(0, self.atualizar_tela_balanca, leitura)

        except serial.SerialException as e:
            self.master.after(0, messagebox.showerror, "Erro", f"Erro na conexão com a porta serial: {e}")
        except Exception as e:
            self.master.after(0, messagebox.showerror, "Erro", f"Ocorreu um erro desconhecido: {e}")

    def atualizar_tela_balanca(self, leitura):
        messagebox.showinfo("Leitura da Balança", f"Peso lido: {leitura} kg")
