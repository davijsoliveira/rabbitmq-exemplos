import pika

# Conecta-se ao servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declara uma fila
queue_name = 'sd-queue'
channel.queue_declare(queue=queue_name, durable=True)

# Publica dez mensagens na fila
for i in range(1,11):
    message = f'Mensagem {i}'
    channel.basic_publish(exchange='sd.direct', routing_key=queue_name, body=message)
    print(f'Mensagem publicada: {message}')

