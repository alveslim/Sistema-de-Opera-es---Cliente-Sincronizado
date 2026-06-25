# Sistema de Operações - Cliente Sincronizado 🚀

Este é o aplicativo cliente desenvolvido em Python utilizando a biblioteca **CustomTkinter**. Ele se conecta a uma API REST para monitorar e confirmar a operação de "tickets" em tempo real, contando com um sistema de atualização automática e tratamento de falhas de conexão.

## 🛠️ Recursos e Funcionalidades

* **Interface Moderna (GUI):** Construída com CustomTkinter, oferecendo suporte nativo ao tema do sistema (Dark/Light mode).
* **Monitoramento em Tempo Real:** Atualização automática a cada 1 segundo (`after(1000)`) sem travar a interface.
* **Tratamento de Erros de Rede:** Desativação automática de botões e alertas visuais caso o servidor fique offline.
* **Ações Síncronas:** Envio de confirmações imediatas via requisições HTTP POST.

---

## 📋 Pré-requisitos

Antes de rodar o cliente, você precisa ter o Python instalado e as seguintes bibliotecas:

```bash
pip install customtkinter requests

    ⚠️ Importante: Este aplicativo depende de um servidor backend rodando para funcionar corretamente. Certifique-se de que a API está ativa no endereço correto.

⚙️ Configuração

Abra o arquivo do código e ajuste a variável global SERVIDOR_URL com o IP e porta correspondentes ao seu backend:
Python

SERVIDOR_URL = "http://localhost:5000"  # Altere para o IP do seu servidor

🚀 Como Executar

Com o servidor já em execução, basta rodar o script do cliente:
Bash

python nome_do_seu_arquivo.py

🛠️ Endpoints Consumidos pela API

O cliente espera que o servidor responda nos seguintes caminhos:

    GET /ticket: Retorna o estado atual do painel.

        Resposta esperada (JSON): {"ticket_atual": 101}

    POST /confirmar: Envia a confirmação do ticket atual.

        Payload enviado (JSON): {"ticket": 101}


---

## 💻 O Código do Cliente (`app.py`)

Aqui está o seu código pronto para ser salvo:

```python
import customtkinter as ctk
import requests

# Configuração do Servidor
SERVIDOR_URL = "http://localhost:5000"  # Substitua pelo IP do seu servidor

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("System")  # "System", "Dark" ou "Light"
ctk.set_default_color_theme("blue")  # "blue", "green" ou "dark-blue"

class AppCliente(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Operações - Sincronizado")
        self.geometry("450x350")
        self.resizable(False, False)

        self.ultimo_ticket_visto = None

        # --- Elementos da Interface (Widgets) ---
        
        # Título principal
        self.lbl_titulo = ctk.CTkLabel(
            self, text="OPERAÇÃO ATUAL", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_titulo.pack(pady=(30, 5))

        # Quadro central que vai destacar o número do ticket
        self.frame_ticket = ctk.CTkFrame(self, width=300, height=100)
        self.frame_ticket.pack(pady=10)
        self.frame_ticket.pack_propagate(False) # Mantém o tamanho fixo do frame

        # O número do ticket propriamente dito
        self.lbl_ticket = ctk.CTkLabel(
            self.frame_ticket, text="---", font=ctk.CTkFont(size=42, weight="bold"), text_color="#1f538d"
        )
        self.lbl_ticket.place(relx=0.5, rely=0.5, anchor="center")

        # Status da conexão/mensagem do servidor
        self.lbl_status = ctk.CTkLabel(
            self, text="Conectando ao servidor...", font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.lbl_status.pack(pady=10)

        # Botão para Confirmar e Avançar
        self.btn_confirmar = ctk.CTkButton(
            self, text="Confirmar e Avançar", font=ctk.CTkFont(size=14, weight="bold"),
            command=self.acao_confirmar, height=45, fg_color="green", hover_color="darkgreen"
        )
        self.btn_confirmar.pack(pady=(20, 10), ipadx=20)

        # Inicia o loop de monitoramento automático do servidor
        self.monitorar_servidor()

    def buscar_dados_servidor(self):
        """Busca o estado atual do ticket no servidor."""
        try:
            resposta = requests.get(f"{SERVIDOR_URL}/ticket", timeout=2)
            if resposta.status_code == 200:
                return resposta.json()
        except requests.exceptions.ConnectionError:
            return None
        return None

    def monitorar_servidor(self):
        """Checa o servidor a cada 1 segundo para atualizar a tela."""
        dados = self.buscar_dados_servidor()

        if dados:
            ticket_atual = dados["ticket_atual"]
            self.lbl_status.configure(text="Conectado ao servidor", text_color="green")
            self.btn_confirmar.configure(state="normal") # Ativa o botão se a rede está OK
            
            # Só atualiza o texto da tela se o ticket realmente mudou
            if ticket_atual != self.ultimo_ticket_visto:
                self.lbl_ticket.configure(text=str(ticket_atual))
                self.ultimo_ticket_visto = ticket_atual
        else:
            self.lbl_status.configure(text="Erro de Conexão! Tentando reconectar...", text_color="red")
            self.lbl_ticket.configure(text="---")
            self.btn_confirmar.configure(state="disabled") # Desativa o botão se não há rede
            self.ultimo_ticket_visto = None

        # O segredo do CustomTkinter: agenda esta mesma função para rodar daqui a 1000ms (1 segundo)
        self.after(1000, self.monitorar_servidor)

    def acao_confirmar(self):
        """Função disparada quando o usuário clica no botão verde."""
        if self.ultimo_ticket_visto:
            try:
                payload = {"ticket": self.ultimo_ticket_visto}
                resposta = requests.post(f"{SERVIDOR_URL}/confirmar", json=payload, timeout=2)
                
                if resposta.status_code == 200:
                    self.lbl_status.configure(text="Ticket confirmado com sucesso!", text_color="green")
                    # Força uma checagem imediata para não ter que esperar 1 segundo para mudar a tela
                    self.monitorar_servidor()
                else:
                    erro_msg = resposta.json().get('erro', 'Erro desconhecido')
                    self.lbl_status.configure(text=f"Erro: {erro_msg}", text_color="orange")
            except requests.exceptions.ConnectionError:
                self.lbl_status.configure(text="Erro de rede ao confirmar.", text_color="red")

if __name__ == "__main__":
    app = AppCliente()
    app.mainloop()
