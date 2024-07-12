##
import os

MICROSERVICE_URLS_dev = {
    'MS-Canoas': 'http://localhost:5002',
    'MS-Reservas': 'http://localhost:5003',    
    'MS-Avaliacoes': 'http://localhost:5004'
}

MICROSERVICE_URLS_prod = {
    'MS-Canoas': 'http://vaalugar-canoas:5000',
    'MS-Reservas': 'http://vaalugar-reservas:5000',
    'MS-Avaliacoes': 'http://vaalugar-avaliacoes:5000'
}

# Determine o modo de execução
devmode = os.getenv('DEVMODE', 'False') == 'True'

if devmode:
    MICROSERVICE_URLS = MICROSERVICE_URLS_dev
else:
    MICROSERVICE_URLS = MICROSERVICE_URLS_prod







def model_dump(self, **kwargs):
        # Substituímos o método `dict` por `model_dump` conforme a depreciação do Pydantic
        return self.dict(**kwargs)

from suporte import *
