from pydantic import BaseModel
from typing import List, Optional

class CanoeQueryRequest(BaseModel):
    local: Optional[str]
    tipos: Optional[List[str]]

class Canoe(BaseModel):
    id: int
    nome: str
    tipo: str
    dono: str
    local: str

class CanoeQueryResponse(BaseModel):
    canoas: List[Canoe]
