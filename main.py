import os

import bcrypt
import mysql.connector
import mysql.connector
import tkinter as tk
from produto.produto import BancoDeDados



class UsuarioDAO:
    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='loja'
        )

    def criar_usuario(self, nome, email, senha, telefone):
        cursor = self.__conexao.cursor()
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO usuarios (nome, email, senha, telefone) VALUES (%s, %s, %s, %s)',
                       (nome, email, hashed, telefone))
        self.__conexao.commit()
        cursor.close()

    def buscar_usuario_por_email(self, email):
        cursor = self.__conexao.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario

    def buscar_usuario_por_id(self, id):
        cursor = self.__conexao.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario


class Usuario:
    def __init__(self, nome, email, senha):
        self.__nome = nome
        self.__email = email
        self.__senha = senha

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        self.__nome = nome

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_senha(self):
        return self.__senha


class LoginWindow:
    def __init__(self, dao):
        self.__dao = dao

        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("400x250")
        self.window.resizable(False, False)  # Impede o redimensionamento

        tk.Label(self.window, width=60, text="Email", font=("Helvetica", 10)).pack()
        self.email_entry = tk.Entry(self.window, width=30, font=("Helvetica", 16))
        self.email_entry.pack()

        tk.Label(self.window, width=60, text="Senha", font=("Helvetica", 10)).pack()
        self.senha_entry = tk.Entry(self.window, show="*", width=30, font=("Helvetica", 16))
        self.senha_entry.pack()

        tk.Button(self.window, text="Login", command=self.login, font=("Helvetica", 10)).pack(side=tk.LEFT, padx=40)
        tk.Button(self.window, text="Criar conta", command=self.abrir_janela_cadastro, font=("Helvetica", 10)).pack(
            side=tk.RIGHT, padx=40)

    def abrir_janela_cadastro(self):
        CadastroWindow(self.__dao)

    def login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        usuario = self.__dao.buscar_usuario_por_email(email)
        if usuario:
            if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha'].encode('utf-8')):
                print("Login realizado com sucesso!")
                caminho_absoluto = os.path.abspath("produto/produto.py")
                # Fechar a janela de login
                self.window.destroy()
                # Execute o arquivo usando a função "exec()"
                with open(caminho_absoluto) as f:
                    code = compile(f.read(), caminho_absoluto, 'exec')
                    exec(code)
            else:
                print("Senha incorreta!")
        else:
            print("Usuário não encontrado!")


class CadastroWindow:
    def __init__(self, dao):
        self.__dao = dao

        self.window = tk.Toplevel()
        self.window.title("Cadastro")
        self.window.geometry("300x150")

        tk.Label(self.window, text="Nome").grid(row=0)
        tk.Label(self.window, text="Email").grid(row=1)
        tk.Label(self.window, text="Senha").grid(row=2)
        tk.Label(self.window, text="Telefone").grid(row=3)

        self.nome_entry = tk.Entry(self.window)
        self.nome_entry.grid(row=0, column=1)

        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=1, column=1)

        self.senha_entry = tk.Entry(self.window, show="*")
        self.senha_entry.grid(row=2, column=1)

        self.telefone_entry = tk.Entry(self.window)
        self.telefone_entry.grid(row=3, column=1)

        tk.Button(self.window, text="Criar conta", command=self.criar_conta).grid(row=4, columnspan=2, pady=10)

    def criar_conta(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        telefone = self.telefone_entry.get()

        self.__dao.criar_usuario(nome, email, senha, telefone)
        print("Conta criada com sucesso!")
        self.window.destroy()


if __name__ == '__main__':
    dao = UsuarioDAO()
    LoginWindow(dao)
    tk.mainloop()
