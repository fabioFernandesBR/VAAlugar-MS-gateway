import requests
from flask import jsonify
from typing import List

from suporte import MICROSERVICE_URLS

from schemas.pesquisa_reservas import SchemaUsuario, Reserva, Avaliacao, ReservasUsuarioResponse



def combina_reservas_avaliacoes(reservas: List[dict], avaliacoes: List[dict]) -> dict:
    resultado = []
    
    for reserva in reservas:
        id_reserva = reserva['id-reserva']
        print(id_reserva)
        encontrado = False
        
        for avaliacao in avaliacoes:
            if avaliacao['idReserva'] == id_reserva:
                resultado.append({
                    'canoa': reserva['canoa'],
                    'data': reserva['data'],
                    'id-reserva': id_reserva,
                    'usuario': reserva['usuario'],
                    'idpost': avaliacao['idPost'],
                    'nota': avaliacao['nota'],
                    'comentario': avaliacao['comentario']
                })
                encontrado = True
                print(resultado)
                break
        
        if not encontrado:
            resultado.append({
                'canoa': reserva['canoa'],
                'data': reserva['data'],
                'id-reserva': id_reserva,
                'usuario': reserva['usuario'],
                'idpost': None,
                'nota': None,
                'comentario': None
            })
    
    return resultado




def listar_reservas(body):
    usuario = body.idusuario
    
    # Chamada ao microsserviço de reservas
    reservas_url = f"{MICROSERVICE_URLS['MS-Reservas']}/reservas-usuario?telefone={usuario}"
    try:
        response_reservas = requests.get(reservas_url)
        response_reservas.raise_for_status()
        reservas = response_reservas.json()['reservas']
        print(reservas)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao obter reservas do microsserviço de reservas: {str(e)}")
    
    # Chamada GraphQL ao microsserviço de avaliações
    graphql_url = f"{MICROSERVICE_URLS['MS-Avaliacoes']}/graphql"
    query = """
    query {
        posts (idUsuario: "%s") {
            idCanoa
            nota
            comentario
            idReserva
            idPost
        }
    }
    """ % usuario
  
    try:
        response_avaliacoes = requests.post(graphql_url, json={'query': query})
        response_avaliacoes.raise_for_status()
        avaliacoes = response_avaliacoes.json()['data']['posts']
        print(avaliacoes)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao obter avaliações do microsserviço de avaliações: {str(e)}")
    

    # Combinando reservas e avaliações em um único JSON
    reservas_avaliacoes = combina_reservas_avaliacoes(reservas, avaliacoes)

    # Retorne a resposta final como JSON
    return jsonify({"reservas": reservas_avaliacoes})