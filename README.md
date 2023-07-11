# Introduction 
This is an API that receives a cpf, value and installment of a credit simulation in JSON format, and returns the offer that has the value and the installment less than or equal to the simulated data. 
Sending the cpf is necessary to check and storing the cache.

# Getting Started

1. Create a venv environment and activate it:

    python3 -m venv venv
    
    . venv/bin/activate

2. Install the required packages:
    
    pip3 install -r requirements.txt

## Running the Application

1. Have a file named .env with the following template:
    
    BASE_URL=
    CLIENT_ID=
    CLIENT_SECRET=

2. Run the application:

    python3 index.py

3. Make a POST request at this endpoint with this json example in body:

    endpoint: POST - "http://127.0.0.1:5000/emprestimos"
    
    BodyJSON:
    {
        "valor": 800,
        "parcela": 16
        "cpf": 99999999999
    }

4. Try again with the same CPF value in JSON to test cache.

5. Try a low value to test the situation where there is no matching offer

     BodyJSON:
    {
        "valor": 50,
        "parcela": 5
        "cpf": 99999999999
    }
