import customtkinter as ctk
from geradorOp import search_Op, grifLoad
import pandas as pd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Table View")
root.geometry("600x400")

# dados_planilha = [
#     ["OP", "Status", "Data"],
#     ["101", "Atiuvo", "01/06"],
#     ["OP", "Pendente", "02/06"],
#     ["OP", "Concluido", "03/06"],
# ]
dados_planilha = search_Op()
print(dados_planilha)

def grifar_op(button):
        button.configure(
            fg_color="#ff4444",
            font=ctk.CTkFont(size=13, overstrike=True), 
            state="disabled"
        )

# Create a frame with roll (case the table it's big)
frame_table = ctk.CTkScrollableFrame(root, width=550, height=300)
frame_table.pack(pady=20, padx=20, fill="both", expand=True)

for num_row, row in enumerate(dados_planilha):
    for num_column, valuer in enumerate(row):
        if num_row == 0:
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
            
            # Commons rows of data
            # Alternate colors of background for give effect "zebra" (optional)
            backgroundColor = "#2a2a2a" if num_row % 2 == 0 else "#222222"
            componente = ctk.CTkButton(
                frame_table, 
                text=valuer, 
                width=150,
                height=30,
                font=ctk.CTkFont(size=13),
                fg_color=backgroundColor,
                hover_color="#14375e",
                command=grifLoad
            )
            componente.configure(command=lambda b=componente: grifar_op(b))
            
        componente.grid(row=num_row, column=num_column, padx=5, pady=2, sticky="nsew")

root.mainloop()