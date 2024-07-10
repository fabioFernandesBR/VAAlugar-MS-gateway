import requests
from flask import jsonify
from typing import List

from suporte import MICROSERVICE_URLS
from suporte import model_dump


from schemas.posta_avaliacao import AvaliacaoRequest


def postar_avaliacao(body):
    try:
        # Recebe os dados da requisição
        # Convertendo AvaliacaoRequest para dicionário Python
        print(body)
        payload = {
            'id_reserva': str(body.id_reserva),
            'id_usuario': body.usuario,  # Corrigido para 'id_usuario' de acordo com a chamada cURL
            'id_canoa': str(body.id_canoa),
            'nota': str(body.nota),  # Convertendo para string para o envio multipart/form-data
            'comentario': body.comentario
        }
        print(payload)

        # Chamada ao microsserviço de avaliações para registrar a avaliação
        avaliacoes_url = f"{MICROSERVICE_URLS['MS-Avaliacoes']}/criar"
        
        response_avaliacoes = requests.post(avaliacoes_url, files={k: (None, str(v)) for k, v in payload.items()})
        response_avaliacoes.raise_for_status()
        avaliacao_response = response_avaliacoes.json()
        print(avaliacao_response)

        # Chamada PATCH ao microsserviço de gerenciamento de canoas para atualização das informações
        gerir_canoas_url = f"{MICROSERVICE_URLS['MS-Canoas']}/atualizaravaliacao"
        payload_patch = {
            'id_canoa': avaliacao_response['id_canoa'],
            'media_avaliacoes': avaliacao_response['nova media de avaliações'],
            'qtde_avaliacoes': avaliacao_response['nova quantidade de avaliações']
        }
        print(payload_patch)
        response_patch = requests.patch(gerir_canoas_url, json=payload_patch)
        response_patch.raise_for_status()
        print("response patch:")
        print(response_patch)
        print("avaliação response:")
        print(avaliacao_response)

        # Monta a resposta final
        resposta_final = {
            'mensagem': 'Avaliação registrada com sucesso.',
            'detalhes': {
                'id_reserva': avaliacao_response['id_reserva'],
                'id_canoa': avaliacao_response['id_canoa'],
                'nota': avaliacao_response['nota'],
                'comentario': avaliacao_response['comentário'],
                'nova_media': avaliacao_response['nova media de avaliações'],
                'nova_quantidade': avaliacao_response['nova quantidade de avaliações']
            }
        }

        return jsonify(resposta_final), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
