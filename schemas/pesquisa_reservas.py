from pydantic import BaseModel, Field
from typing import List, Optional

class SchemaUsuario(BaseModel):
    idusuario: str = Field(..., description="Número de telefone do usuário.")

class Reserva(BaseModel):
    canoa: int
    data: str
    id_reserva: int
    usuario: str
    

class Avaliacao(BaseModel):
    idCanoa: int
    nota: float
    comentario: str
    idReserva: int
    idPost: int

class Reserva_com_Avaliacao(BaseModel):
    canoa: int
    data: str
    id_reserva: int
    nota: Optional[float] = None
    comentario: Optional[str] = None
    idPost: Optional[int] = None

class ReservasUsuarioResponse(BaseModel):
    reservas_completas: List[Reserva_com_Avaliacao]

