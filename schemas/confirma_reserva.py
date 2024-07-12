from pydantic import BaseModel
from typing import Optional, List


class SchemaConfirmacaoReserva(BaseModel):
    """ 
    Define como uma nova reserva a ser criada deve ser representada, 
    do usuário para a API. 

    Método POST
    """
    usuario: str = "21999999999"
    canoa: int = 1
    data: str = "01/05/2025" 


class SchemaVisualizacaoReservaConfirmada(BaseModel):
    """ Define como uma nova reserva recém criada deve ser representada, 
    da API para o usuário.
    """
    id_reserva: int = 1
    usuario: str = "21999999999"
    canoa: int = 1
    data: str = "01/05/2025"
    
