import requests

from flask import jsonify

from suporte import MICROSERVICE_URLS
from suporte import model_dump
from schemas.mensagem_erro import ErrorResponse
from schemas.consulta_canoas import Canoe, CanoeQueryResponse


def consulta_canoas(body):
    print(body)
    query = """
    query getCanoes($local: String, $tipos: [String!]) {
      canoas(local: $local, tipos: $tipos) {
        nome
        tipo
        estado
        municipio
        bairro
        referencia
        mediaAvaliacoes
        qtdeAvaliacoes
        idcanoa
      }
    }
    """
    # Convertendo o corpo da requisição em um dicionário
    variables = body.model_dump()
    print(variables)
    
    # Construindo a URL do microsserviço
    url = f"{MICROSERVICE_URLS['MS-Canoas']}/graphql"
    
    try:
        # Fazendo a requisição POST para o endpoint GraphQL com a query e as variáveis
        response = requests.post(url, json={'query': query, 'variables': variables})
        print(response)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Tratando exceções e retornando uma resposta de erro
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 400
    
    # Processando a resposta
    data = response.json()
    print(data)
    canoes_data = data['data']['canoas']

    canoes = []
    for canoa_data in canoes_data:
        canoe = Canoe(
            id=canoa_data.get('idcanoa'),
            nome=canoa_data.get('nome'),
            tipo=canoa_data.get('tipo'),
            estado=canoa_data.get('estado'),
            municipio=canoa_data.get('municipio'),
            bairro=canoa_data.get('bairro'),
            referencia=canoa_data.get('referencia'),
            mediaAvaliacoes=canoa_data.get('mediaAvaliacoes'),
            qtdeAvaliacoes=canoa_data.get('qtdeAvaliacoes')
        )
        canoes.append(canoe)

    return jsonify(CanoeQueryResponse(canoas=canoes).model_dump())

