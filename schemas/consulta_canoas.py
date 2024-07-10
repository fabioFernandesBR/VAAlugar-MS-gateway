from pydantic import BaseModel
from typing import List, Optional

class CanoeQueryRequest(BaseModel):
    local: Optional[str]
    tipos: Optional[List[str]]

class Canoe(BaseModel):
    id: int
    nome: str
    tipo: str
    estado: str
    municipio: str
    bairro: Optional[str]
    referencia: Optional[str]
    mediaAvaliacoes: Optional[float]
    qtdeAvaliacoes: Optional[int]

class CanoeQueryResponse(BaseModel):
    canoas: List[Canoe]
