import customtkinter as ctk
import csv

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Table View - Integração Excel")
root.geometry("600x400")

# --- 1. FUNÇÃO PARA CARREGAR OS DADOS DO CSV ---
def carregar_dados():
    try:
        with open("op.csv", "r", encoding="utf-8") as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        # Se o arquivo não existir ainda, criamos uma base de teste
        base_teste = [
            ["OP", "Status", "Data"],
            ["101", "Ativo", "01/06"],
            ["102", "Pendente", "02/06"],
            ["103", "Concluido", "03/06"],
        ]
        salvar_no_excel(base_teste)
        return base_teste

# --- 2. FUNÇÃO PARA SALVAR OS DADOS DE VOLTA NO CSV ---
def salvar_no_excel(dados):
    with open("op.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(dados)

# --- 3. FUNÇÃO DO CLIQUE: GRIFA NA TELA E NO EXCEL ---
def grifar_e_salvar(botao, linha_idx, coluna_idx):
    texto_atual = botao.cget("text")
    
    # Se já tiver sido grifado, não faz nada de novo
    if "[X]" in texto_atual:
        return
        
    # Novo texto com a marcação de baixa para o Excel
    novo_texto = f"[X] {texto_atual}"
    
    # A. Atualiza o dado na nossa lista da memória
    dados_planilha[linha_idx][coluna_idx] = novo_texto
    
    # B. Salva a lista atualizada direto no arquivo op.csv
    salvar_no_excel(dados_planilha)
    
    # C. Atualiza o visual do botão na tela na mesma hora
    botao.configure(
        text=novo_texto,
        font=ctk.CTkFont(size=13, overstrike=True),
        fg_color="#ff4444"
    )
    print(f"Excel atualizado! Linha {linha_idx}, Coluna {coluna_idx} agora é: {novo_texto}")


# --- CONSTRUÇÃO DA INTERFACE ---

# Carrega os dados reais do seu arquivo op.csv
dados_planilha = carregar_dados()

frame_table = ctk.CTkScrollableFrame(root, width=550, height=300)
frame_table.pack(pady=20, padx=20, fill="both", expand=True)

for num_row, row in enumerate(dados_planilha):
    for num_column, valuer in enumerate(row):
        if num_row == 0:
            # Cabeçalho
            componente = ctk.CTkLabel(
                frame_table,
                text=valuer,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#1f538d",
                text_color="white",
                corner_radius=4,
                width=150,
                height=30
            )
        else:
            # Dados
            backgroundColor = "#2a2a2a" if num_row % 2 == 0 else "#222222"
            
            # Se o arquivo já foi aberto com células marcadas como [X],
            # nós já criamos o botão riscado logo de início!
            ja_marcado = "[X]" in valuer
            fonte_botao = ctk.CTkFont(size=13, overstrike=ja_marcado)
            cor_botao = "#ff4444" if ja_marcado else backgroundColor
            
            componente = ctk.CTkButton(
                frame_table, 
                text=valuer, 
                width=150,
                height=30,
                font=fonte_botao,
                fg_color=cor_botao,
                hover_color="#14375e",
            )
            
            # O SEGREDO: Passamos o botão, o número da linha e o da coluna para o lambda
            componente.configure(
                command=lambda b=componente, r=num_row, c=num_column: grifar_e_salvar(b, r, c)
            )
            
        componente.grid(row=num_row, column=num_column, padx=5, pady=2, sticky="nsew")

root.mainloop()