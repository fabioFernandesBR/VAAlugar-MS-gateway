# app.py
from flask import Flask, jsonify, request, redirect
from pydantic import BaseModel, ValidationError
import requests
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from schemas.consulta_previsao import *
from schemas.dicionario_previsao_tempo import dicionario
from schemas.confirma_reserva import *
from schemas.consulta_canoas import *
from xml.etree import ElementTree
import logging
from unidecode import unidecode
from typing import Optional, List

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
reserva_tag = Tag(name = "Confirma Reserva", description = "Confirma reserva")

MICROSERVICE_URLS = {
    'MS-Reservas': 'http://localhost:5001',
    'MS-Canoas': 'http://localhost:5002',
    'MS-Avaliacoes': 'http://localhost:5003'
}

class CanoeQueryRequest(BaseModel):
    local: str = None
    tipos: list[str] = None

class CanoeQueryResponse(BaseModel):
    canoas: list

class ErrorResponse(BaseModel):
    error: str

    def model_dump(self, **kwargs):
        # Substituímos o método `dict` por `model_dump` conforme a depreciação do Pydantic
        return self.dict(**kwargs)

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


## Consulta canoas
@app.post('/consultacanoas', tags=[canoa_tag], responses={"200": CanoeQueryResponse, "400": ErrorResponse})
def pesquisa_canoas(body: CanoeQueryRequest):
    """Pesquisa por canoas disponíveis conforme critérios informados pelo Front End."""
    
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
    
    # Construindo a URL do microsserviço
    url = f"{MICROSERVICE_URLS['MS-Canoas']}/graphql"
    
    try:
        # Fazendo a requisição POST para o endpoint GraphQL com a query e as variáveis
        response = requests.post(url, json={'query': query, 'variables': variables})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Tratando exceções e retornando uma resposta de erro
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 400
    
    # Processando a resposta
    data = response.json()
    canoes = data['data']['canoas']
    return jsonify(CanoeQueryResponse(canoas=canoes).model_dump())

## Consulta à previsão do tempo:

### Funções auxiliares:
def get_city_code(local: str, estado: str) -> str:
    try:
        # Constrói a URL de consulta
        local_unidecode = unidecode(local.lower())
        url = f"http://servicos.cptec.inpe.br/XML/listaCidades?city={local_unidecode}"

        # Faz a requisição HTTP
        response = requests.get(url)
        response.raise_for_status()

        # Parse do XML recebido
        tree = ElementTree.fromstring(response.content)

        # Encontra a cidade correta com o estado correspondente
        for cidade in tree.findall('cidade'):
            if unidecode(cidade.find('nome').text.lower()) == unidecode(local.lower()) and cidade.find('uf').text == estado:
                return cidade.find('id').text
        
        # Se não encontrar, levanta um ValueError
        raise ValueError("Cidade não encontrada")
    
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Erro na requisição HTTP: {str(e)}")
    except (ElementTree.ParseError, ValueError) as e:
        raise ValueError(f"Erro ao parsear XML: {str(e)}")
    except Exception as e:
        raise Exception(f"Erro inesperado: {str(e)}")
    



def get_weather_forecast(city_code: str) -> Optional[List[dict]]:
    try:
        url = f"http://servicos.cptec.inpe.br/XML/cidade/7dias/{city_code}/previsao.xml"
        
        response = requests.get(url)
        response.raise_for_status()
        
        tree = ElementTree.fromstring(response.content)
        
        forecast = []
        for previsao in tree.findall('previsao'):
            dia = previsao.find('dia').text
            
            
            tempo = previsao.find('tempo').text
            tempo_descricao = dicionario.get(tempo, tempo)


            maxima = previsao.find('maxima').text
            minima = previsao.find('minima').text
            iuv = previsao.find('iuv').text
            
            forecast.append({
                'dia': dia,
                'tempo': tempo_descricao,
                'maxima': maxima,
                'minima': minima,
                'iuv': iuv
            })
        
        return forecast
    
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Erro na requisição HTTP: {str(e)}")
    except (ElementTree.ParseError, ValueError) as e:
        raise ValueError(f"Erro ao parsear XML: {str(e)}")
    except Exception as e:
        raise Exception(f"Erro inesperado: {str(e)}")
    


@app.post('/consultaprevisao', tags=[previsao_tag], responses={"200": PrevisaoTempoResponse, "400": ErrorResponse})
def consulta_previsao_tempo(body: PrevisaoTempoRequest):
    """Consulta a previsão do tempo para os próximos 7 dias."""
    try:
        local = body.local
        estado = body.estado

        city_code = get_city_code(local, estado)
        
        # Obtém a previsão do tempo usando o código da cidade
        forecast = get_weather_forecast(city_code)
        
        
        if not forecast:
            return jsonify(ErrorResponse(mensagem="Previsão do tempo não disponível para os próximos 7 dias.").model_dump()), 400
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição HTTP: {str(e)}")
        return jsonify(ErrorResponse(mensagem=f"Erro na requisição HTTP: {str(e)}").model_dump()), 400
    except ValueError as e:
        logging.error(f"Erro de valor: {str(e)}")
        return jsonify(ErrorResponse(mensagem=str(e)).model_dump()), 400
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return jsonify(ErrorResponse(mensagem=f"Erro inesperado: {str(e)}").model_dump()), 500
    
    return jsonify(PrevisaoTempoResponse(cidade= local, estado = estado, previsao=forecast).model_dump()), 200


## Confirma reserva
## Confirma reserva
@app.post('/confirmareserva', 
          tags=[reserva_tag], 
          responses={"200": SchemaVisualizacaoReservaConfirmada, "400": ErrorResponse})
def confirma_reserva(body: SchemaConfirmacaoReserva):
    try:
        # Chamada ao microsserviço de reservas
        url = 'http://localhost:5001/reserva'
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





## gestão dos erros

@app.errorhandler(requests.exceptions.RequestException)
def handle_bad_request(e):
    return jsonify(ErrorResponse(error=str(e)).model_dump()), 400

@app.errorhandler(500)
def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500



## Execução

if __name__ == '__main__':
    app.run(debug=True)
