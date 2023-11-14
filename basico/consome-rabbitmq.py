import pika

# Conecta-se ao servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declara uma fila
queue_name = 'sd-queue'
channel.queue_declare(queue=queue_name, durable=True)

# Callback para processar mensagens recebidas
def callback(ch, method, properties, body):
    print(f'Mensagem recebida: {body.decode()}')

# Consume as mensagens da fila
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens. Para sair, pressione Ctrl+C')
channel.start_consuming()
