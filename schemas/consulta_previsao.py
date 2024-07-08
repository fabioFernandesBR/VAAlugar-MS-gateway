from pydantic import BaseModel, Field
from typing import List, Optional

class PrevisaoDia(BaseModel):
    dia: str
    tempo: str
    maxima: int
    minima: int
    iuv: float

class PrevisaoTempoResponse(BaseModel):
    cidade: str
    estado: str
    previsao: List[PrevisaoDia]

class PrevisaoTempoRequest(BaseModel):
    local: str
    estado: str
