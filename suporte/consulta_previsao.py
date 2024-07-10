import requests
from unidecode import unidecode
import logging

from flask import jsonify
from xml.etree import ElementTree
from typing import Optional, List

from schemas import ErrorResponse, PrevisaoTempoResponse
from schemas.dicionario_previsao_tempo import dicionario
from suporte import model_dump



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






### Função principal:
def consulta_previsao(body):
    try:
        local = body.local
        estado = body.estado

        city_code = get_city_code(local, estado)
        print(f"city code is {city_code}")
        
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
