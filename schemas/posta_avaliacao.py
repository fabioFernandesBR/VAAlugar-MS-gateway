from pydantic import BaseModel, Field

class AvaliacaoRequest(BaseModel):
    id_reserva: int
    usuario: str
    id_canoa: int
    nota: float
    comentario: str

class AvaliacaoResponse(BaseModel):
    mensagem: str = Field(..., description="Mensagem de confirmação.")
    detalhes: dict = Field(..., description="Detalhes da avaliação registrada.",
                           json_schema_extra={"id_reserva": 1, "id_canoa": 10, "nota": 7.5, "comentario": "Ótima experiência.",
                                    "nova_media": 7.8, "nova_quantidade": 15})


