import os
import uvicorn
import requests
from fastapi import FastAPI, Request, status
from fastapi.responses import Response
from dotenv import load_dotenv
from auth.auth import auth
from cache.cache import CPF

app = FastAPI()
load_dotenv()

#Função que recebe o token e chama a API com as ofertas. 
def get_offers(token, value, installments):
    url = f"{os.environ.get('BASE_URL')}/ofertas"
    try:
        headers = {"Authorization": "Bearer " + token}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            offers = response.json()
            print("Offers:  ", offers) #Print mantido para conferência.
            return offers
        else:
            return {"message":"API call error", "StatusCode": response.status_code}

    except Exception as e:
        return {"message": str(e)}

#Rota principal onde o usuário envia, em português, o valor, a parcela e o cpf.
@app.post('/emprestimos')
async def main(request: Request):
    try:
        #Recebe os parametros do usuário
        data = await request.json()
        value = data['valor']
        installments = data['parcela']
        cpf = data['cpf']

        #Confere se o CPF já está cadastrado no cache
        if cpf in CPF.cache:
            client = CPF.cache[cpf]
            cpf_offer = client.check_offers()
            if cpf_offer:
                return {"message":"O cpf já possui uma oferta cadastrada:", "oferta":cpf_offer}
        else:
        #Inicia a autenticação e busca por ofertas
            token = auth()
            offers = get_offers(token, value, installments)
            
            #Filtra as ofertas que se adequam à condição e busca a primeira aparição.
            filtered_offer = (item for item in offers if item['value'] <= value and item['installments'] <= installments) 
            first_offer = next(filtered_offer, False)
            
            if first_offer:
                client = CPF(cpf)
                client.add_offers(first_offer)
                #Retorna ao usuário em português
                return {
                    "identificador": first_offer['id'],
                    "parceiro": first_offer['partner'],
                    "parcelas": first_offer['installments'],
                    "valor": first_offer['value']
                }   
            else:
                #Retorno vazio caso não ache oferta que atenda a condição.
                return Response(status_code = status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return {"message": str(e)}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
