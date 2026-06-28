import time
import requests

# Substitua pelo IP real do computador que está rodando o 'server.py'
# Se testar na mesma máquina do servidor, pode usar 'localhost'
SERVIDOR_URL = "http://192.168.100.105:5000" 

def checar_ticket():
    try:
        resposta = requests.get(f"{SERVIDOR_URL}/ticket")
        if resposta.status_code == 200:
            return resposta.json()
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao servidor.")
    return None

def confirmar_ticket(ticket_atual):
    try:
        payload = {"ticket": ticket_atual}
        resposta = requests.post(f"{SERVIDOR_URL}/confirmar", json=payload)
        if resposta.status_code == 200:
            print("\n[✓] Ticket confirmado com sucesso no servidor!")
            return True
        else:
            print(f"\n[X] Erro ao confirmar: {resposta.json().get('erro')}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão ao tentar confirmar.")
    return False

def main():
    ultimo_ticket_visto = None

    while True:
        dados = checar_ticket()
        
        if dados:
            ticket_atual = dados["ticket_atual"]
            
            # Só limpa a tela e mostra a mensagem se o ticket mudou
            if ticket_atual != ultimo_ticket_visto:
                print("\n" + "="*30)
                print(f" OPERAÇÃO ATUAL: {ticket_atual} ")
                print("="*30)
                print("Pressione 'C' para confirmar e avançar ou 'Enter' para atualizar status...")
                ultimo_ticket_visto = ticket_atual

        # Um input simples para simular a ação do usuário no terminal
        # Em uma interface gráfica (como Tkinter ou Flask web), isso seria um botão
        opcao = input("> ").strip().upper()
        
        if opcao == 'C' and dados:
            confirmar_ticket(dados["ticket_atual"])
        
        # Aguarda 1 segundo antes de atualizar a tela novamente
        time.sleep(1)

if __name__ == "__main__":
    main()