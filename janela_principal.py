from tkinter import *
from crud import *
import customtkinter as ctk

def montar_janela_principal(janela, usuario_id):

    janela.geometry("750x550")
    janela.title("Sistema - Grêmio")

    def atualizar_lista_transacoes():
        # Exemplo de como puxar e atualizar os valores nos cards
        total_receitas = calcular_total("Receita", usuario_id)
        total_saidas = calcular_total("Despesa", usuario_id)
        
        # O saldo total é receita menos despesa
        saldo_total = total_receitas - total_saidas

        # Atualizando as labels dos cards que você criou
        label_valor_entrada.configure(text=f"R$ {total_receitas:.2f}")
        label_valor_saida.configure(text=f"R$ {total_saidas:.2f}")
        label_valor_saldo.configure(text=f"R$ {saldo_total:.2f}")

        if tabela.get() == "Extrato":
            # Limpa todos os widgets antigos de dentro do frame rolável
            for widget in frame.winfo_children():
                widget.destroy()
            
            # Busca os dados atualizados no banco        
            dados_transacoes = gerar_lista_transacoes(usuario_id)

            linha = 0
            for transacao in dados_transacoes:
                tipo, categoria, descricao, valor, data, id_usuario  = transacao

                ctk.CTkLabel(frame, text="{}".format(tipo)).grid(row=linha, column=0, pady=20, padx=10)
                ctk.CTkLabel(frame, text="{}".format(categoria)).grid(row=linha, column=1, pady=20, padx=20)            
                ctk.CTkLabel(frame, text="{}".format(descricao)).grid(row=linha, column=2, pady=20, padx=80)
                ctk.CTkLabel(frame, text="{}".format(valor)).grid(row=linha, column=3, pady=20, padx=40)
                ctk.CTkLabel(frame, text="{}".format(data)).grid(row=linha, column=4, pady=20, padx=5)
                ctk.CTkLabel(frame, text="{}".format(id_usuario)).grid(row=linha, column=5, pady=20, padx=50)

                linha += 1

    # CRIAÇÃO DO TABVIEW
    
    tabela = ctk.CTkTabview(janela, width=350, height=500, command=atualizar_lista_transacoes)
    tabela.pack(pady=10)


    # Criação de Tabelas

    tab_1 = tabela.add("Dashboard") 
    tab_2 = tabela.add("Nova Transação") 
    tab_3 = tabela.add("Extrato")
    #tab_4 = tabela.add("Configurações")

    
    # TABELA 1 - DASHBOARD
    # Saldo
    card_saldo = ctk.CTkFrame(tab_1, corner_radius=10)
    card_saldo.pack(pady=10, padx=20, fill="x")  # fill="x" faz o card ocupar a largura da tela

    label_titulo_saldo = ctk.CTkLabel(card_saldo, text="Saldo Total Atual", font=("Arial", 14, "bold"))
    label_titulo_saldo.pack(pady=(10, 0), padx=15, anchor="w") # anchor="w" alinha o texto à esquerda

    label_valor_saldo = ctk.CTkLabel(card_saldo, text="R$ 0,00", font=("Arial", 24, "bold"), text_color="green")
    label_valor_saldo.pack(pady=(5, 10), padx=15, anchor="w")

    # Entrada
    card_entrada = ctk.CTkFrame(tab_1, corner_radius=10)
    card_entrada.pack(pady=10, padx=20, fill="x")

    label_titulo_entrada = ctk.CTkLabel(card_entrada, text="Total de Entradas do Mês")
    label_titulo_entrada.pack(pady=(10, 0), padx=15, anchor="w") # anchor="w" alinha o texto à esquerda

    label_valor_entrada = ctk.CTkLabel(card_entrada, text="R$ 0,00", font=("Arial", 24, "bold"), text_color="#0065A8")
    label_valor_entrada.pack(pady=(5, 10), padx=15, anchor="w")

    # Saída
    card_saida = ctk.CTkFrame(tab_1, corner_radius=10)
    card_saida.pack(pady=10, padx=20, fill="x")

    label_titulo_saida = ctk.CTkLabel(card_saida, text="Total de Saídas do Mês")
    label_titulo_saida.pack(pady=(10, 0), padx=15, anchor="w") # anchor="w" alinha o texto à esquerda

    label_valor_saida = ctk.CTkLabel(card_saida, text="R$ 0,00", font=("Arial", 24, "bold"), text_color="red")
    label_valor_saida.pack(pady=(5, 10), padx=15, anchor="w")


    # TABELA 2 - NOVA TRANSAÇÃO
    categorias_por_tipo = {
        "Receita": ["Salário", "Freelance", "Investimentos", "Outros"],
        "Despesa": ["Alimentação", "Transporte", "Lazer", "Moradia", "Contas"]
    }

    # Função que atualiza as opções da categoria automaticamente quando o tipo muda
    def atualizar_categorias(tipo_escolhido):
        campo_resultado.configure(text="")
        novas_opcoes = categorias_por_tipo[tipo_escolhido]
        selecionar_categoria.configure(values=novas_opcoes)
        selecionar_categoria.set(novas_opcoes[0]) # Seleciona a primeira opção por padrão

    def salvar_transacao():
        tipo = selecionar_tipo.get()
        categoria = selecionar_categoria.get()  # Pega a categoria selecionada
        descricao = campo_descricao.get().lower()
        valor = campo_valor.get()
        data = campo_data.get().strip()

        if tipo and descricao and valor and data:
            try:
                valor_formatado = float(valor.replace(",", "."))

                cadastrar_transacao(categoria, tipo, descricao, valor_formatado, data, usuario_id)

                campo_resultado.configure(text="Transação Cadastrada!")

                campo_descricao.delete(0, "end")
                campo_valor.delete(0, "end")
                campo_data.delete(0, "end")
                

            except ValueError:
                campo_resultado.configure(text="Erro: Digite um valor numérico válido!", text_color="red")


    # 1. Menu de Tipo (chama a função atualizar_categorias quando muda)
    selecionar_tipo = ctk.CTkOptionMenu(tab_2, values=list(categorias_por_tipo.keys()), command=atualizar_categorias)
    selecionar_tipo.pack(pady=10)

    # 2. Menu de Categoria (começa mostrando as opções de "Receita")
    selecionar_categoria = ctk.CTkOptionMenu(tab_2, values=categorias_por_tipo["Receita"])
    selecionar_categoria.pack(pady=10)

    campo_descricao = ctk.CTkEntry(tab_2, placeholder_text="Descrição")
    campo_descricao.pack(pady=10)

    campo_valor = ctk.CTkEntry(tab_2, placeholder_text="Valor")
    campo_valor.pack(pady=10)

    campo_data = ctk.CTkEntry(tab_2, placeholder_text="Data: dd/mm/yyyy")
    campo_data.pack(pady=10)

    botao_salvar = ctk.CTkButton(tab_2, text="Salvar", command=salvar_transacao)
    botao_salvar.pack(pady=10)

    campo_resultado = ctk.CTkLabel(tab_2, text='', font=("Arial", 20))
    campo_resultado.pack(pady=10)


    # TABELA 3 - EXTRATO
    cabecalho = ctk.CTkFrame(tab_3)
    cabecalho.pack(fill="x", padx=20, pady=(10, 0))

    ctk.CTkLabel(cabecalho, text="Tipo", font=("Arial", 15)).grid(row=0, column=1, padx=10)
    ctk.CTkLabel(cabecalho, text="Categoria", font=("Arial", 15)).grid(row=0, column=2, padx=30)
    ctk.CTkLabel(cabecalho, text="Descrição", font=("Arial", 15)).grid(row=0, column=3, padx=90)
    ctk.CTkLabel(cabecalho, text="Valor", font=("Arial", 15)).grid(row=0, column=4, padx=20)
    ctk.CTkLabel(cabecalho, text="Data", font=("Arial", 15)).grid(row=0, column=5, padx=15)
    ctk.CTkLabel(cabecalho, text="Usuário", font=("Arial", 15)).grid(row=0, column=6, padx=15)

    # Criando o Scrollable Frame
    frame = ctk.CTkScrollableFrame(tab_3,
                                width=650,
                                height=500,
                                )
    frame.pack(pady=40)