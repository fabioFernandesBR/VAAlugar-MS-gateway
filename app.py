# app.py
import requests
import logging

from flask import jsonify, redirect
from pydantic import BaseModel
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

from schemas.consulta_previsao import PrevisaoTempoRequest, PrevisaoTempoResponse
from schemas.confirma_reserva import SchemaConfirmacaoReserva, SchemaVisualizacaoReservaConfirmada
from schemas.consulta_canoas import CanoeQueryRequest, CanoeQueryResponse
from schemas.mensagem_erro import SchemaMensagemErro, ErrorResponse
from schemas.pesquisa_reservas import SchemaUsuario, ReservasUsuarioResponse
from schemas.posta_avaliacao import AvaliacaoResponse, AvaliacaoRequest
from suporte.consulta_canoas import consulta_canoas
from suporte.consulta_previsao import consulta_previsao
from suporte.confirma_reserva import confirma_reserva
from suporte.lista_reservas import listar_reservas
from suporte.posta_avaliacao import postar_avaliacao
from suporte import model_dump






# Configuração de logging
logging.basicConfig(level=logging.DEBUG)


# Informações da API para documentação
info = Info(title="VAAlugar-MS Gateway", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição dos tags para a documentação
home_tag = Tag(name="Home", description="Redireciona para a documentação da API")
canoa_tag = Tag(name="Canoas", description="Pesquisa e informações sobre canoas")
previsao_tag = Tag(name="Previsão do Tempo", description="Previsão do Tempo")
reserva_tag = Tag(name = "Gestão de Reservas", description = "Confirmação e busca de reservas")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')




## Consulta canoas:
@app.post('/consultacanoas', tags=[canoa_tag], responses={"200": CanoeQueryResponse, "400": ErrorResponse})
def pesquisa_canoas(body: CanoeQueryRequest):
    try:
        resultado = consulta_canoas(body)
        return resultado, 200
    except Exception as e:
        app.logger.error(f"Exception on /consultacanoas [POST]: {e}")
        return jsonify({'error': str(e)}), 500





## Consulta à previsão do tempo:
@app.post('/consultaprevisao', tags=[previsao_tag], responses={"200": PrevisaoTempoResponse, "400": ErrorResponse})
def consulta_previsao_tempo(body: PrevisaoTempoRequest):
    '''Consulta a previsão do tempo para os próximos 7 dias.'''
    try:
        resultado = consulta_previsao(body)
        return resultado
    except Exception as e:
        app.logger.error(f"Exception on /consultacanoas [POST]: {e}")
        return jsonify({'error': str(e)}), 500

    






## Confirma reserva
@app.post('/confirmareserva', 
          tags=[reserva_tag], 
          responses={"200": SchemaVisualizacaoReservaConfirmada, "400": ErrorResponse})
def confirmacao_reserva(body: SchemaConfirmacaoReserva):
    try:
        resultado = confirma_reserva(body)
        return resultado
    except Exception as e:
        app.logger.error(f"Exception on /consultacanoas [POST]: {e}")
        return jsonify({'error': str(e)}), 500
    
    
    
## Listagem de Reservas
@app.post('/listarreservas', 
          tags=[reserva_tag], 
          responses={"200": ReservasUsuarioResponse, "400": ErrorResponse})
def listar_reservas_usuario(body: SchemaUsuario):
    try:
        resultado = listar_reservas(body)
        return resultado
    except Exception as e:
        app.logger.error(f"Exception on /listarreservas [POST]: {e}")
        return jsonify({'error': str(e)}), 500

   

## Postar avaliação
@app.post('/avaliar', 
          tags=[reserva_tag], 
          responses={"200": AvaliacaoResponse, "400": ErrorResponse})
def postar_avaliacao_reserva(body: AvaliacaoRequest):
    try:
        resultado = postar_avaliacao(body)
        return resultado
    except Exception as e:
        app.logger.error(f"Exception on /listarreservas [POST]: {e}")
        return jsonify({'error': str(e)}), 500





## gestão dos erros

@app.errorhandler(requests.exceptions.RequestException)
def handle_bad_request(e):
    return jsonify(ErrorResponse(error=str(e)).model_dump()), 400

@app.errorhandler(500)
def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500



## Execução

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

