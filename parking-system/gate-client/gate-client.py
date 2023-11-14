import requests

def check_ticket():
    try:
        url = 'http://localhost:8081/check/4' 
        response = requests.get(url)

        if response.status_code == 200:
            ticket = response.json()
            print(f"Número: {ticket['numero']}, Valor: {ticket['valor']}, Tempo: {ticket['tempo']}")
        else:
            print(f"Erro: {response.status_code} - {response.json().get('erro')}")

    except Exception as e:
        print(f"Erro na solicitação: {str(e)}")

if __name__ == '__main__':
    check_ticket()
