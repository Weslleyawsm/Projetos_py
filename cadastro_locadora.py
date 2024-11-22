import pyodbc
from tkinter import *
from tkinter import ttk
import mysql.connector


conexao = mysql.connector.connect(
    host="localhost", user="root", password="1234", database="carros")
cursor = conexao.cursor()


def verifica_credenciais():
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="1234", database="carros")
    cursor = conexao.cursor()

    cursor.execute("Select * From usuarios Where nome=%s And senha=%s",
                   (nome_entry.get(), senha_entry.get()))
    usuario = cursor.fetchone()

    def listar_inventario():
        for i in treeview1.get_children():
            treeview1.delete(i)
        cursor.execute("select * from inventario")
        valores = cursor.fetchall()
        for valor in valores:
            treeview1.insert("", "end", values=(
                valor[0], valor[1], valor[2], valor[3], valor[4], valor[5]))

    def listar_cliente():
        for i in treeview2.get_children():
            treeview2.delete(i)
        cursor.execute("select * from cliente")
        valores = cursor.fetchall()
        for valor in valores:
            treeview2.insert("", "end", values=(
                valor[0], valor[1], valor[2], valor[3]))

    def listar_marcas():
        for i in treeview3.get_children():
            treeview3.delete(i)
        cursor.execute("select * from marcas")
        valores = cursor.fetchall()
        for valor in valores:
            treeview3.insert("", "end", values=(
                valor[0], valor[1], valor[2]))

    def listar_alugados():
        for i in treeview4.get_children():
            treeview4.delete(i)
        cursor.execute("select * from alugados")
        valores = cursor.fetchall()
        for valor in valores:
            treeview4.insert("", "end", values=(
                valor[0], valor[1], valor[2], valor[3], valor[4]))
    if usuario:
        janela_principal.destroy()
        tabela = Tk()
        
        style = ttk.Style(tabela)
        global treeview1
        treeview1 = ttk.Treeview(tabela, style="mystyle.Treeview")
        style.theme_use("default")
        style.configure("mystyle.Treeview", font=("Arial", 14))
        treeview1 = ttk.Treeview(tabela, style="mystyle.Treeview", columns=(
            "id", "modelo", "transmissao", "motor", "combustivel", "marcas_id"), show="headings", height=20)
        treeview1.heading("id", text="ID")
        treeview1.heading("modelo", text="Modelo")
        treeview1.heading("transmissao", text="Transmissão")
        treeview1.heading("motor", text="Motor")
        treeview1.heading("combustivel", text="Combustivel")
        treeview1.heading("marcas_id", text="ID Marcas")

        treeview1.column("#0", width=0, stretch=NO)
        treeview1.column("id", width=80)
        treeview1.column("modelo", width=120)
        treeview1.column("transmissao", width=170)
        treeview1.column("motor", width=120)
        treeview1.column("combustivel", width=150)
        treeview1.column("marcas_id", width=120)

        treeview1.grid(row=8, column=0, columnspan=10, sticky="NSEW")
        listar_inventario()

        def tb_inventario():
            style = ttk.Style(tabela)
            global treeview1
            treeview1 = ttk.Treeview(tabela, style="mystyle.Treeview")
            style.theme_use("default")
            style.configure("mystyle.Treeview", font=("Arial", 14))
            treeview1 = ttk.Treeview(tabela, style="mystyle.Treeview", columns=(
                "id", "modelo", "transmissao", "motor", "combustivel", "marcas_id"), show="headings", height=20)
            treeview1.heading("id", text="ID")
            treeview1.heading("modelo", text="Modelo")
            treeview1.heading("transmissao", text="Transmissão")
            treeview1.heading("motor", text="Motor")
            treeview1.heading("combustivel", text="Combustivel")
            treeview1.heading("marcas_id", text="ID Marcas")

            treeview1.column("#0", width=0, stretch=NO)
            treeview1.column("id", width=80)
            treeview1.column("modelo", width=120)
            treeview1.column("transmissao", width=170)
            treeview1.column("motor", width=120)
            treeview1.column("combustivel", width=150)
            treeview1.column("marcas_id", width=120)

            treeview1.grid(row=8, column=0, columnspan=10, sticky="NSEW")

            def listar_inventario():
                for i in treeview1.get_children():
                    treeview1.delete(i)
                cursor.execute("select * from inventario")
                valores = cursor.fetchall()
                for valor in valores:
                    treeview1.insert("", "end", values=(
                        valor[0], valor[1], valor[2], valor[3], valor[4], valor[5]))
            
            listar_inventario()
           
        def tb_cliente():
            style = ttk.Style(tabela)
            global treeview2
            treeview2 = ttk.Treeview(tabela, style="mystyle.Treeview")
            style.theme_use("default")
            style.configure("mystyle.Treeview", font=("Arial", 14))
            treeview2 = ttk.Treeview(tabela, style="mystyle.Treeview", columns=(
                "id", "nome", "sobrenome", "endereco"), show="headings", height=20)
            treeview2.heading("id", text="ID")
            treeview2.heading("nome", text="Nome")
            treeview2.heading("sobrenome", text="Sobrenome")
            treeview2.heading("endereco", text="Endereço")

            treeview2.column("#0", width=0, stretch=NO)
            treeview2.column("id", width=80)
            treeview2.column("nome", width=120)
            treeview2.column("sobrenome", width=170)
            treeview2.column("endereco", width=300)

            treeview2.grid(row=8, column=0, columnspan=10, sticky="NSEW")

            def listar_cliente():
                for i in treeview2.get_children():
                    treeview2.delete(i)
                cursor.execute("select * from cliente")
                valores = cursor.fetchall()
                for valor in valores:
                    treeview2.insert("", "end", values=(
                        valor[0], valor[1], valor[2], valor[3]))
            listar_cliente()

        def tb_marcas():
            style = ttk.Style(tabela)
            global treeview3
            treeview3 = ttk.Treeview(tabela, style="mystyle.Treeview")
            style.theme_use("default")
            style.configure("mystyle.Treeview", font=("Arial", 14))
            treeview3 = ttk.Treeview(tabela, style="mystyle.Treeview", columns=(
                "id", "marcas_carros", "origem"), show="headings", height=20)
            treeview3.heading("id", text="ID")
            treeview3.heading("marcas_carros", text="Marca do Carro")
            treeview3.heading("origem", text="País de Origem")

            treeview3.column("#0", width=0, stretch=NO)
            treeview3.column("id", width=40)
            treeview3.column("marcas_carros", width=120)
            treeview3.column("origem", width=170)

            treeview3.grid(row=8, column=0, columnspan=10, sticky="NSEW")

            def listar_dados():
                for i in treeview3.get_children():
                    treeview1.delete(i)
                cursor.execute("select * from marcas")
                valores = cursor.fetchall()
                for valor in valores:
                    treeview3.insert("", "end", values=(
                        valor[0], valor[1], valor[2]))
            listar_dados()

        def tb_alugados():
            style = ttk.Style(tabela)
            global treeview4
            treeview4 = ttk.Treeview(tabela, style="mystyle.Treeview")
            style.theme_use("default")
            style.configure("mystyle.Treeview", font=("Arial", 14))
            treeview4 = ttk.Treeview(tabela, style="mystyle.Treeview", columns=(
                "id", "cliente", "modelo", "tipo_de_aluguel", "data_inicio"), show="headings", height=20)
            treeview4.heading("id", text="ID")
            treeview4.heading("cliente", text="Cliente")
            treeview4.heading("modelo", text="Modelo")
            treeview4.heading("tipo_de_aluguel", text="Tipo de Aluguel")
            treeview4.heading("data_inicio", text="Data de Início")

            treeview4.column("#0", width=0, stretch=NO)
            treeview4.column("id", width=80)
            treeview4.column("cliente", width=120)
            treeview4.column("modelo", width=170)
            treeview4.column("tipo_de_aluguel", width=120)
            treeview4.column("data_inicio", width=150)

            treeview4.grid(row=8, column=0, columnspan=10, sticky="NSEW")

            listar_alugados()

        tabela.geometry("810x600")
        tabela.configure(bg="#404641")

        inventario = Button(tabela, text="Inventário",
                            bg="#AEB7AF", width=24, borderwidth=4, relief="raised", command=tb_inventario).grid(row=0, column=0)
        cliente = Button(tabela, text="Cliente",
                         bg="#AEB7AF", width=28, borderwidth=4, relief="raised", command=tb_cliente).grid(row=0, column=1)
        marcas = Button(tabela, text="Marcas",
                        bg="#AEB7AF", width=28, borderwidth=4, relief="raised", command=tb_marcas).grid(row=0, column=2)
        alugados = Button(tabela, text="Alugados",
                          bg="#AEB7AF", width=28, borderwidth=4, relief="raised", command=tb_alugados).grid(row=0, column=3)

        def add_inventario():

            jan_inventario = Tk()
            jan_inventario.geometry("340x450")
            jan_inventario.configure(bg="#404641")

            def salvar_dados():
                dados_inventario = (entry_modelo.get(), entry_transmissao.get(
                ), entry_motor.get(), entry_combustivel.get(), entry_marcaID.get())
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='1234',
                    database='carros')
                sql = "INSERT INTO inventario (modelo, transmissao, motor, combustivel, marcas_id) VALUES (%s, %s, %s, %s, %s)"
                cursor = conexao.cursor()
                cursor.execute(sql, dados_inventario)
                conexao.commit()
                jan_inventario.destroy()

                def listar_inventario():
                    for i in treeview1.get_children():
                        treeview1.delete(i)
                    cursor.execute("select * from inventario")
                    valores = cursor.fetchall()
                    for valor in valores:
                        treeview1.insert("", "end", values=(
                            valor[0], valor[1], valor[2], valor[3], valor[4], valor[5]))
                listar_inventario()
            Label(jan_inventario, text="Modelo", width=15, bg="#3333ff").grid(
                row=1, column=0, padx=0, pady=30, sticky="W")
            entry_modelo = Entry(jan_inventario, width=25, font=("Arial 10"))
            entry_modelo.grid(row=1, column=1, padx=20, pady=29, sticky="W")

            Label(jan_inventario, text="Transmissão", width=15, bg="#3333ff").grid(
                row=2, column=0, padx=0, pady=30, sticky="W")  
            entry_transmissao = Entry(
                jan_inventario, width=25, font=("Arial 10"))
            entry_transmissao.grid(
                row=2, column=1, padx=20, pady=29, sticky="W")

            Label(jan_inventario, text="Motor", width=15, bg="#3333ff").grid(
                row=3, column=0, padx=0, pady=30, sticky="W")
            entry_motor = Entry(jan_inventario, width=25, font=("Arial 10"))
            entry_motor.grid(row=3, column=1, padx=20, pady=29, sticky="W")

            Label(jan_inventario, text="Combustível", width=15, bg="#3333ff").grid(
                row=4, column=0, padx=0, pady=30, sticky="W")
            entry_combustivel = Entry(
                jan_inventario, width=25, font=("Arial 10"))
            entry_combustivel.grid(
                row=4, column=1, padx=20, pady=29, sticky="W")

            Label(jan_inventario, text="Marca ID", width=15, bg="#3333ff").grid(
                row=5, column=0, padx=0, pady=30, sticky="W")
            entry_marcaID = Entry(jan_inventario, width=25, font=("Arial 10"))
            entry_marcaID.grid(row=5, column=1, padx=20, pady=29, sticky="W")

            btn_salvar = Button(jan_inventario, width=15, text="Salvar", bg="green", command=salvar_dados).grid(
                row=6, column=0, padx=10)
            btn_cancelar = Button(jan_inventario, width=15, text="Cancelar", bg="red",
                                  command=jan_inventario.destroy).grid(row=6, column=1, padx=10)

            jan_inventario.mainloop()

        def delete_inventario():
            selecionar_invt = treeview1.selection()
            if not selecionar_invt:
                # Ou uma mensagem de aviso para o usuário
                print("Nada selecionado!")
                return  # Retorna se nada estiver selecionado
            selecionar_invt = treeview1.selection()[0]
            id = treeview1.item(selecionar_invt)['values'][0]
            cursor.execute("delete from inventario where id = %s", (id,))
            conexao.commit()
            listar_inventario()

        def add_cliente():
            jan_cliente = Tk()
            jan_cliente.geometry("340x450")
            jan_cliente.configure(bg="#404641")

            def salvar_dados():
                dados_inventario = (entry_id.get(), entry_nome.get(
                ), entry_sobrenome.get(), entry_endereco.get())
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='1234',
                    database='carros')
                sql = "INSERT INTO cliente (id, nome, sobrenome, endereco) VALUES (%s, %s, %s, %s)"
                cursor = conexao.cursor()
                cursor.execute(sql, dados_inventario)
                conexao.commit()
                jan_cliente.destroy()

                def listar_cliente():
                    for i in treeview2.get_children():
                        treeview2.delete(i)
                    cursor.execute("select * from cliente")
                    valores = cursor.fetchall()
                    for valor in valores:
                        treeview2.insert("", "end", values=(
                            valor[0], valor[1], valor[2], valor[3]))
                listar_cliente()

            Label(jan_cliente, text="ID", width=15, bg="#3333ff").grid(
                row=0, column=0, padx=0, pady=20, sticky="NW")
            entry_id = Entry(jan_cliente, width=25, font=("Arial 10"))
            entry_id.grid(row=0, column=1, padx=0, pady=0, sticky="W")

            Label(jan_cliente, text="Nome", width=15, bg="#3333ff").grid(
                row=1, column=0, padx=0, pady=80, sticky="NW")
            entry_nome = Entry(jan_cliente, width=25, font=("Arial 10"))
            entry_nome.grid(row=1, column=1, padx=0, pady=40, sticky="W")

            Label(jan_cliente, text="Sobrenome", width=15, bg="#3333ff").grid(
                row=2, column=0, padx=0, pady=0, sticky="NW")
            entry_sobrenome = Entry(jan_cliente, width=25, font=("Arial 10"))
            entry_sobrenome.grid(row=2, column=1, padx=0, pady=0, sticky="NW")

            Label(jan_cliente, text="Endereço", width=15, bg="#3333ff").grid(
                row=3, column=0, padx=0, pady=80, sticky="NW")
            entry_endereco = Entry(jan_cliente, width=25, font=("Arial 10"))
            entry_endereco.grid(row=3, column=1, padx=0, pady=80, sticky="NW")

            btn_salvar = Button(jan_cliente, width=15, text="Salvar", bg="green", command=salvar_dados).grid(
                row=3, column=0, pady=120, sticky="Nw")
            btn_cancelar = Button(jan_cliente, width=15, text="Cancelar", bg="red", command=jan_cliente.destroy).grid(
                row=3, column=1, pady=120, padx=30, sticky="Nw")
            jan_cliente.mainloop()

        def delete_cliente():
            selecionar_clint = treeview2.selection()
            if not selecionar_clint:
                # Ou uma mensagem de aviso para o usuário
                print("Nada selecionado!")
                return  # Retorna se nada estiver selecionado
            selecionar_clint = treeview2.selection()[0]
            id = treeview2.item(selecionar_clint)['values'][0]
            cursor.execute("delete from cliente where id = %s", (id,))
            conexao.commit()
            listar_cliente()

        def add_marcas():

            jan_marcas = Tk()
            jan_marcas.geometry("330x200")
            jan_marcas.configure(bg="#404641")

            def salvar_marcas():
                dados = (entry_marca.get(), entry_origem.get())
                conexao = mysql.connector.connect(
                    host='localhost', user='root', password='1234', database='carros')
                sql = "INSERT INTO marcas (marcas_carros, origem) VALUES(%s, %s)"
                cursor = conexao.cursor()
                cursor.execute(sql, dados)
                conexao.commit()
                jan_marcas.destroy()

                def listar_marcas():
                    for i in treeview3.get_children():
                        treeview3.delete(i)
                    cursor.execute("select * from marcas")
                    valores = cursor.fetchall()
                    for valor in valores:
                        treeview3.insert("", "end", values=(
                            valor[0], valor[1], valor[2]))
                listar_marcas()

            Label(jan_marcas, text="Marca do Carro", width=15, bg="#3333ff").grid(
                row=0, column=0, padx=0, pady=20, sticky="NW")
            entry_marca = Entry(jan_marcas, width=25, font=("Arial 10"))
            entry_marca.grid(row=0, column=1, padx=10, pady=0, sticky="W")

            Label(jan_marcas, text="País de Origem", width=15, bg="#3333ff").grid(
                row=1, column=0, pady=20, sticky="NW")
            entry_origem = Entry(jan_marcas, width=25, font=("Arial 10"))
            entry_origem.grid(row=1, column=1, pady=20, padx=10, sticky="NW")

            btn_salvar = Button(jan_marcas, text="Salvar", bg="green",
                                command=salvar_marcas, width=15).grid(row=2, column=0)
            btn_cancelar = Button(jan_marcas, text="Cancelar", bg="red",
                                  command=jan_marcas.destroy, width=15).grid(row=2, column=1)
            jan_marcas.mainloop()

        def delete_marcas():
            selection_marca = treeview3.selection()
            if not selection_marca:
                print("Nada Selecionado!")
                return
            selection_marca = treeview3.selection()[0]
            id = treeview3.item(selection_marca)['values'][0]
            cursor.execute("delete from marcas where id=%s", (id,))
            conexao.commit()
            listar_marcas()

        def add_alugados():
            jan_alugados = Tk()
            jan_alugados.geometry("350x350")
            jan_alugados.configure(bg="#404641")

            def salvar_alugados():
                dados = (entry_id_cliente.get(), entry_id_modelo.get(),
                         entry_tipo_aluguel.get(), entry_data_inicio.get())
                conexao = mysql.connector.connect(
                    host='localhost', user='root', password='1234', database='carros')
                sql = "INSERT INTO alugados (cliente, modelo, tipo_de_aluguel, data_inicio) VALUES(%s, %s, %s, %s)"
                cursor = conexao.cursor()
                cursor.execute(sql, dados)
                conexao.commit()
                jan_alugados.destroy()

                def listar_alugados():
                    for i in treeview4.get_children():
                        treeview4.delete(i)
                    cursor.execute("select * from alugados")
                    valores = cursor.fetchall()
                    for valor in valores:
                        treeview4.insert("", "end", values=(
                            valor[0], valor[1], valor[2], valor[3], valor[4]))
                listar_alugados()

            Label(jan_alugados, text="ID Cliente", width=15,
                  bg="#3333ff").grid(row=0, column=0, pady=20)
            entry_id_cliente = Entry(jan_alugados, width=20, font=("Arial 10"))
            entry_id_cliente.grid(row=0, column=1, padx=10, pady=20)

            Label(jan_alugados, text="ID Modelo", width=15,
                  bg="#3333ff").grid(row=1, column=0, pady=20)
            entry_id_modelo = Entry(jan_alugados, width=20, font=("Arial 10"))
            entry_id_modelo.grid(row=1, column=1, padx=10, pady=20)

            Label(jan_alugados, text="Tipo de Aluguel", width=15,
                  bg="#3333ff").grid(row=2, column=0, pady=20)
            entry_tipo_aluguel = Entry(
                jan_alugados, width=20, font=("Arial 10"))
            entry_tipo_aluguel.grid(row=2, column=1, padx=10, pady=20)

            Label(jan_alugados, text="Data de Inicio", width=15,
                  bg="#3333ff").grid(row=3, column=0, pady=20)
            entry_data_inicio = Entry(
                jan_alugados, width=20, font=("Arial 10"))
            entry_data_inicio.grid(row=3, column=1, padx=10, pady=20)

            btn_salvar = Button(jan_alugados, text="Salvar", bg="green",
                                command=salvar_alugados, width=15).grid(row=4, column=0)
            btn_cancelar = Button(jan_alugados, text="Cancelar", bg="red",
                                  command=jan_alugados.destroy, width=15).grid(row=4, column=1)
            jan_alugados.mainloop()

        def delete_alugados():
            selection_alugados = treeview4.selection()
            if not selection_alugados:
                print("Nada Selecionado")
            selection_alugados = treeview4.selection()[0]
            id = treeview4.item(selection_alugados)['values'][0]
            cursor.execute("delete from alugados where id=%s", (id,))
            conexao.commit()
            listar_alugados()

        btn_inventario = Button(tabela, text="Adicionar no Inventário", bg="#009900", width=24,
                                borderwidth=4, relief="raised", command=add_inventario).grid(row=9, column=0)
        del_dados = Button(tabela, text="Deletar do Inventário", bg="#990000", width=24,
                           borderwidth=4, relief="raised", command=delete_inventario).grid(row=10, column=0)

        btn_cliente = Button(tabela, text="Adicionar Cliente", bg="#009900", width=24,
                             borderwidth=4, relief="raised", command=add_cliente).grid(row=9, column=1, sticky="E")
        del_cliente = Button(tabela, text="Deletar Cliente", bg="#990000", width=24, borderwidth=4,
                             relief="raised", command=delete_cliente).grid(row=10, column=1, sticky="E")

        btn_marcas = Button(tabela, text="Adicionar Marcas", bg="#009900", width=24, borderwidth=4,
                            relief="raised", command=add_marcas).grid(row=9, column=2, sticky="E")
        del_marca = Button(tabela, text="Deletar Marcas", bg="#990000", width=24, borderwidth=4,
                           relief="raised", command=delete_marcas).grid(row=10, column=2, sticky="E")

        btn_alugados = Button(tabela, text="Adicionar Alugados", bg="#009900", width=24, borderwidth=4,
                              relief="raised", command=add_alugados).grid(row=9, column=3, sticky="E")
        del_alugados = Button(tabela, text="Deletar do Alugados", bg="#990000", width=24, borderwidth=4,
                              relief="raised", command=delete_alugados).grid(row=10, column=3, sticky="E")

        tabela.mainloop()

    else:
        Label(janela_principal, text="Usuário ou Senha incorretos!",
              fg="red").grid(row=7, columnspan=2)
    cursor.close()
    conexao.close()


janela_principal = Tk()
janela_principal.title("Tela de Login")
janela_principal.configure(bg="#F5F5F5")

# CENTRALIZANDO A JANELA NA TELA DO COMPUTADOR
# pre definindo a altura e largura da janela
larg_janela = 400
alt_janela = 270

# winfo_screenwidth puxa a medida da tela do computador
larg_tela = janela_principal.winfo_screenwidth()
alt_tela = janela_principal.winfo_screenheight()

pos_x = (larg_tela // 2) - (larg_janela // 2)
pos_y = (alt_tela // 2) - (alt_janela // 2)

janela_principal.geometry(
    '{}x{}+{}+{}'.format(larg_janela, alt_janela, pos_x, pos_y))

title_lbl = Label(janela_principal, text="Tela de Login",
                  fg="blue", bg="#F5F5F5", font="Arial 20")
title_lbl.grid(row=0, column=0, columnspan=2, pady=20)

nome_lbl = Label(janela_principal, text="Nome do Usuário ", font="Arial 14")
nome_lbl.grid(row=1, column=0, pady=5)
nome_entry = Entry(janela_principal, font="Arial 14")
nome_entry.grid(row=1, column=1, pady=5, stick="e")

senha_lbl = Label(janela_principal, text="Senha",
                  bg="#F5F5F5", font="Arial 14")
senha_lbl.grid(row=2, column=0, pady=5, stick="e")
senha_entry = Entry(janela_principal, font="Arial 14", show="*")
senha_entry.grid(row=2, column=1, pady=5)

entrar_btn = Button(janela_principal, text="Entrar",
                    bg="green", command=verifica_credenciais)
entrar_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")
sair_btn = Button(janela_principal, text="Sair",
                  command=janela_principal.destroy,
                  bg="red")
sair_btn.grid(row=5, column=0, columnspan=2, padx=20, stick="NSEW")

janela_principal.mainloop()

cursor.close()
conexao.close()
