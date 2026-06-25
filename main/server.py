from flask import Flask, jsonify, request

app = Flask(__name__)

# Estado inicial do sistema
dados_sistema = {
    "ticket_atual": 37000,
    "status": "Aguardando confirmação"
}

@app.route('/ticket', methods=['GET'])
def obter_ticket():
    """Retorna o ticket atual para as máquinas visualizarem."""
    return jsonify(dados_sistema)

@app.route('/confirmar', methods=['POST'])
def confirmar_ticket():
    """Avança para o próximo ticket quando o usuário clica em confirmar."""
    dados_cliente = request.json
    ticket_recebido = dados_cliente.get("ticket")

    # Garante que o cliente está confirmando o ticket correto
    if ticket_recebido == dados_sistema["ticket_atual"]:
        dados_sistema["ticket_atual"] += 1  # Passa para a próxima operação
        dados_sistema["status"] = f"Ticket {ticket_recebido} confirmado! Próxima operação iniciada."
        return jsonify({"sucesso": True, "novo_ticket": dados_sistema["ticket_atual"]})
    else:
        return jsonify({"sucesso": False, "erro": "Ticket enviado está desatualizado."}), 400

if __name__ == '__main__':
    # '0.0.0.0' permite que o servidor seja acessado por outros computadores na mesma rede
    # Escolha uma porta livre, por exemplo, 5000
    app.run(host='0.0.0.0', port=5000, debug=True)