import customtkinter as ctk
import requests
import threading

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppCliente(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Operações - Sincronizado")
        self.geometry("450x420") # Aumentei um pouco a altura para caber o novo campo
        self.resizable(False, False)

        self.ultimo_ticket_visto = None
        # O URL agora é uma variável que pertence à interface, começando no localhost
        self.servidor_url = "http://localhost:5000"

        # --- NOVA SEÇÃO: Configuração de IP ---
        self.frame_config = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_config.pack(pady=(15, 0), padx=20, fill="x")

        self.lbl_ip = ctk.CTkLabel(self.frame_config, text="IP do Servidor:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_ip.pack(side="left", padx=(0, 10))

        # Caixa de texto onde você vai digitar o IP
        self.entry_ip = ctk.CTkEntry(self.frame_config, placeholder_text="Ex: 192.168.0.10", width=140)
        self.entry_ip.insert(0, "localhost") # Já começa escrito localhost por padrão
        self.entry_ip.pack(side="left", padx=(0, 10))

        # Botão para salvar/atualizar o IP
        self.btn_atualizar_ip = ctk.CTkButton(self.frame_config, text="Conectar", width=90, command=self.atualizar_ip)
        self.btn_atualizar_ip.pack(side="left")
        # ----------------------------------------

        # --- Elementos da Interface (Widgets) ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="OPERAÇÃO ATUAL", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_titulo.pack(pady=(20, 5))

        self.frame_ticket = ctk.CTkFrame(self, width=300, height=100)
        self.frame_ticket.pack(pady=10)
        self.frame_ticket.pack_propagate(False)

        self.lbl_ticket = ctk.CTkLabel(
            self.frame_ticket, text="---", font=ctk.CTkFont(size=42, weight="bold"), text_color="#1f538d"
        )
        self.lbl_ticket.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_status = ctk.CTkLabel(
            self, text="Conectando ao servidor...", font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.lbl_status.pack(pady=10)

        self.btn_confirmar = ctk.CTkButton(
            self, text="Confirmar e Avançar", font=ctk.CTkFont(size=14, weight="bold"),
            command=self.acao_confirmar, height=45, fg_color="green", hover_color="darkgreen"
        )
        self.btn_confirmar.pack(pady=(15, 10), ipadx=20)

        # Inicia o loop de monitoramento automático
        self.monitorar_servidor()

    def atualizar_ip(self):
        """Função disparada ao clicar no botão 'Conectar' ao lado do IP"""
        ip_digitado = self.entry_ip.get().strip()
        
        if not ip_digitado:
            return
            
        # Limpa formatações se o usuário digitar algo extra sem querer
        ip_digitado = ip_digitado.replace("http://", "").replace("https://", "")
        
        # Se o usuário não digitou a porta, adicionamos a porta 5000 automaticamente
        if ":" not in ip_digitado:
            ip_digitado = f"{ip_digitado}:5000"
            
        # Atualiza a URL que o sistema vai usar nas requisições
        self.servidor_url = f"http://{ip_digitado}"
        
        # Dá um feedback visual e força a limpeza do ticket atual na tela
        self.lbl_status.configure(text=f"Conectando a {ip_digitado}...", text_color="orange")
        self.ultimo_ticket_visto = None 

    def buscar_dados_servidor(self):
        try:
            # Agora usamos self.servidor_url no lugar da variável global
            resposta = requests.get(f"{self.servidor_url}/ticket", timeout=2)
            if resposta.status_code == 200:
                return resposta.json()
        except requests.exceptions.ConnectionError:
            return None
        return None

    def monitorar_servidor(self):
        thread = threading.Thread(target=self._tarefa_monitorar, daemon=True)
        thread.start()
        
        self.after(1000, self.monitorar_servidor)

    def _tarefa_monitorar(self):
        dados = self.buscar_dados_servidor()

        if dados:
            ticket_atual = dados["ticket_atual"]
            self.lbl_status.configure(text="Conectado ao servidor", text_color="green")
            self.btn_confirmar.configure(state="normal")
            
            if ticket_atual != self.ultimo_ticket_visto:
                self.lbl_ticket.configure(text=str(ticket_atual))
                self.ultimo_ticket_visto = ticket_atual
        else:
            self.lbl_status.configure(text="Erro de Conexão! Verifique o IP.", text_color="red")
            self.lbl_ticket.configure(text="---")
            self.btn_confirmar.configure(state="disabled")
            self.ultimo_ticket_visto = None

    def acao_confirmar(self):
        thread = threading.Thread(target=self._tarefa_confirmar, daemon=True)
        thread.start()

    def _tarefa_confirmar(self):
        if self.ultimo_ticket_visto:
            self.btn_confirmar.configure(state="disabled")
            self.lbl_status.configure(text="Confirmando...", text_color="gray")
            
            try:
                payload = {"ticket": self.ultimo_ticket_visto}
                # Agora usamos self.servidor_url no post também
                resposta = requests.post(f"{self.servidor_url}/confirmar", json=payload, timeout=2)
                
                if resposta.status_code == 200:
                    self.lbl_status.configure(text="Ticket confirmado com sucesso!", text_color="green")
                else:
                    erro_msg = resposta.json().get('erro', 'Erro desconhecido')
                    self.lbl_status.configure(text=f"Erro: {erro_msg}", text_color="orange")
            except requests.exceptions.ConnectionError:
                self.lbl_status.configure(text="Erro de rede ao confirmar.", text_color="red")
            finally:
                self.btn_confirmar.configure(state="normal")

if __name__ == "__main__":
    app = AppCliente()
    app.mainloop()