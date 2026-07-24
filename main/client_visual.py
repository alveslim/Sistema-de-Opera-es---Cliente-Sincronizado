import customtkinter as ctk
import threading
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppCliente(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Operações - Google Sheets")
        self.geometry("450x350")
        self.resizable(False, False)

        self.ultimo_ticket_visto = None
        self.bloqueio_atualizacao = False  # Evita conflito de leitura enquanto escreve

        # --- Configuração Inicial do Google Sheets ---
        self.inicializar_sheets()

        # --- Elementos da Interface (Widgets) ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="OPERAÇÃO ATUAL (Célula A1)", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_titulo.pack(pady=(30, 5))

        self.frame_ticket = ctk.CTkFrame(self, width=300, height=100)
        self.frame_ticket.pack(pady=10)
        self.frame_ticket.pack_propagate(False)

        self.lbl_ticket = ctk.CTkLabel(
            self.frame_ticket, text="---", font=ctk.CTkFont(size=42, weight="bold"), text_color="#1f538d"
        )
        self.lbl_ticket.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_status = ctk.CTkLabel(
            self, text="Conectando ao Google Sheets...", font=ctk.CTkFont(size=12), text_color="orange"
        )
        self.lbl_status.pack(pady=10)

        self.btn_confirmar = ctk.CTkButton(
            self, text="Confirmar e Avançar", font=ctk.CTkFont(size=14, weight="bold"),
            command=self.acao_confirmar, height=45, fg_color="green", hover_color="darkgreen"
        )
        self.btn_confirmar.pack(pady=(15, 10), ipadx=20)
        self.btn_confirmar.configure(state="disabled")

        # Inicia o loop de monitoramento automático
        self.monitorar_servidor()

    def inicializar_sheets(self):
        """Autentica na API do Google Sheets usando um dicionário embutido no código"""
        try:
            # Dicionário com as credenciais da Service Account
            creds_dict = {
                xxxxxxx
            }
            
            scopes = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]

            # Mudança aqui: usando from_json_keyfile_dict em vez de from_json_keyfile_name
            creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict=creds_dict, scopes=scopes)
            client = gspread.authorize(creds)

            nome_planilha = "xxxx"
            id_pasta = 'xxxxxxxx'
            
            # Conecta à planilha
            self.planilha = client.open(title=nome_planilha, folder_id=id_pasta).get_worksheet(0)
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            self.planilha = None

    def monitorar_servidor(self):
        """Dispara a thread de leitura do Sheets de tempos em tempos"""
        # Só lê se não estivermos no meio de um processo de escrita
        if not self.bloqueio_atualizacao:
            thread = threading.Thread(target=self._tarefa_monitorar, daemon=True)
            thread.start()
        
        # Agenda a próxima verificação para dali a 2000ms (2 segundos) para evitar estourar cota da API
        self.after(2000, self.monitorar_servidor)

    def _tarefa_monitorar(self):
        if not self.planilha:
            self.lbl_status.configure(text="Erro: Falha na conexão com o Sheets.", text_color="red")
            return

        try:
            # Pega o valor da célula A1
            dado = self.planilha.acell('A1').value
            
            if dado is not None:
                self.lbl_status.configure(text="Sincronizado com Google Sheets", text_color="green")
                if not self.bloqueio_atualizacao:
                    self.btn_confirmar.configure(state="normal")
                
                # Se o valor na planilha mudou, atualiza a interface
                if dado != self.ultimo_ticket_visto:
                    self.lbl_ticket.configure(text=str(dado))
                    self.ultimo_ticket_visto = dado
        except Exception as e:
            self.lbl_status.configure(text="Erro ao ler dados da planilha.", text_color="red")
            self.btn_confirmar.configure(state="disabled")

    def acao_confirmar(self):
        """Disparado ao clicar no botão verde"""
        # Bloqueia o monitoramento temporariamente para evitar conflito de threads
        self.bloqueio_atualizacao = True
        self.btn_confirmar.configure(state="disabled")
        self.lbl_status.configure(text="Atualizando planilha...", text_color="orange")
        
        thread = threading.Thread(target=self._tarefa_confirmar, daemon=True)
        thread.start()

    def _tarefa_confirmar(self):
        try:
            # Pega o valor atual da tela e calcula o próximo
            valor_atual = self.lbl_ticket.cget("text")
            
            if valor_atual == "---":
                novo_valor = 1
            else:
                novo_valor = int(valor_atual) + 1
                
            # Salva o novo valor direto na célula A1 (sobrescrevendo)
            self.planilha.update_acell('A1', novo_valor)
            
            # Atualiza localmente para dar resposta imediata na interface
            self.lbl_ticket.configure(text=str(novo_valor))
            self.ultimo_ticket_visto = str(novo_valor)
            self.lbl_status.configure(text="Planilha atualizada com sucesso!", text_color="green")
            
        except Exception as e:
            self.lbl_status.configure(text="Erro ao atualizar célula A1.", text_color="red")
        finally:
            # Libera o app para voltar a monitorar
            self.bloqueio_atualizacao = False
            self.btn_confirmar.configure(state="normal")

if __name__ == "__main__":
    app = AppCliente()
    app.mainloop()