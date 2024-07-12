import requests
import logging

from flask import jsonify

from suporte import MICROSERVICE_URLS
from suporte import model_dump
from schemas.mensagem_erro import ErrorResponse
from schemas.confirma_reserva import SchemaVisualizacaoReservaConfirmada


def confirma_reserva(body):
    print(body)
    try:
        # Chamada ao microsserviço de reservas
        url = f"{MICROSERVICE_URLS['MS-Reservas']}/reserva"
        payload = {
            'canoa': body.canoa,
            'usuario': body.usuario,
            'data': body.data
        }
        print(payload)
        response = requests.post(url, data=payload)
        
        # Verifica se a resposta foi bem-sucedida (código 200)
        if response.status_code == 200:
            # Se a reserva foi criada com sucesso, retorna os dados da reserva
            reserva_data = response.json()
             
            reserva_response = SchemaVisualizacaoReservaConfirmada(
                id_reserva=reserva_data.get('id-reserva'),
                canoa=reserva_data.get('canoa'),
                usuario=reserva_data.get('usuario'),
                data=reserva_data.get('data')
            )
            return jsonify(reserva_response.model_dump())
        else:
            # Se ocorreu algum erro, retorna uma resposta de erro
            error_detail = f"Erro ao criar reserva: {response.text}"
            return ErrorResponse(error=error_detail)
    
    except Exception as e:
        # Se ocorrer algum erro inesperado, retorna um erro interno do servidor
        logging.error(f"Erro ao confirmar reserva: {str(e)}")
        return ErrorResponse(error="Erro interno do servidor"), 500
