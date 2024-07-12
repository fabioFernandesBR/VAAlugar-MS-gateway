##


# Isso funcionava no VS Code
'''MICROSERVICE_URLS = {
    'MS-Reservas': 'http://localhost:5001',
    'MS-Canoas': 'http://localhost:5002',
    'MS-Avaliacoes': 'http://localhost:5003'
}'''

# Para rodar dentro da Docker (??):
MICROSERVICE_URLS = {
    'MS-Reservas': 'http://VAAlugar-Reservas:5000',
    'MS-Canoas': 'http://VAAlugar-Canoas:5000',
    'MS-Avaliacoes': 'http://VAAlugar-Avaliacoes:5000'
}






def model_dump(self, **kwargs):
        # Substituímos o método `dict` por `model_dump` conforme a depreciação do Pydantic
        return self.dict(**kwargs)

from suporte import *