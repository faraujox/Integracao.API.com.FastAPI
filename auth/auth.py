import os
import requests

#Função de autenticação: Busca os parametros no .env e chama a rota /autenticar da api por um post
def auth():
    url = f"{os.environ.get('BASE_URL')}/autenticar"
    try:
        params = {
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('CLIENT_SECRET')
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url, params=params, headers=headers)
        
        #Em caso de resposta 200, envia o token para buscar as ofertas.
        if response.status_code == 200:
            token = response.json()["access_token"]
            return token
        elif response.status_code == 401:
            return {"message": "Invalid credentials", "StatusCode": response.status_code}
        else:
            return {"message": "Authentication Fails", "StatusCode": response.status_code}
    except Exception as e:
            return {"message": str(e)}