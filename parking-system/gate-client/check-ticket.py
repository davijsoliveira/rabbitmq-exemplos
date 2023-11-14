import json
import threading
import time
from pika import BlockingConnection, BasicProperties
from flask import Flask, jsonify

app = Flask(__name__)

# Tickets pagos
tickets = []

# Configura a conexão com o RabbitMQ
connection = BlockingConnection()
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}") # Imprime a mensagem recebida
    json_body = json.loads(body.decode()) # Converte a mensagem de string para json    
    tickets.append(json_body) # Adiciona a mensagem na lista de tickets pagos
    print(tickets) # Imprime a lista de tickets pagos
    ch.basic_ack(delivery_tag=method.delivery_tag) # Confirma que a mensagem foi entregue

def consume_messages():
    channel.basic_qos(prefetch_count=1) # Configura o buffer para 1 mensagem por vez
    channel.basic_consume(queue='parking-queue', on_message_callback=callback) # Realiza o consumo das mensagens utilizando uma função de callback
    channel.start_consuming() # Inicia o consumo

# Cria uma thread para consumir mensagens
thread = threading.Thread(target=consume_messages) 
thread.start()

# Rota para verificar se o ticket apresentado na cancela já foi pago
@app.route('/check/<int:numero>', methods=['GET'])
def check_ticket(numero):
    try:
        for ticket in tickets:
            if ticket['numero'] == numero:
                return jsonify(ticket)
    except Exception as e:
        return jsonify({'erro': str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)


