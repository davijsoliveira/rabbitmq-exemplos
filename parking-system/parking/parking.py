import json
from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

# Tickets pagos
tickets = []

def connect_queue(message):
    try:
        # Conecta-se ao servidor RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Declara uma fila
        queue_name = 'parking-queue'
        channel.queue_declare(queue=queue_name, durable=True)
        # Publica a mensagem
        channel.basic_publish(exchange='parking.direct',
                              routing_key=queue_name,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                              ))
    except Exception as e:
        print(f"Erro ao enviar mensagem para a fila: {str(e)}")

@app.route('/payed', methods=['POST'])
def pay():
    try:
        data = request.json
        numero = data.get('numero')
        valor = data.get('valor')
        tempo = data.get('tempo')
        ticket = {'numero': numero, 'valor': valor, 'tempo': tempo}
        tickets.append(ticket)
        print(tickets)
        ticket_json = json.dumps(ticket)
        connect_queue(ticket_json)
        print(f'Mensagem publicada!')
        return jsonify({'mensagem': 'Ticket cadastro com sucesso'})
    
    except Exception as e:
        return jsonify({'erro': str(e)})

@app.route('/list', methods=['GET'])
def list():
    try:
        return jsonify(tickets)
    except Exception as e:
        return jsonify({'erro': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
