from pydantic import BaseModel


class SchemaMensagemErro(BaseModel):
    """ Define como uma mensagem de erro será representada.
    """
    message: str = "Algo deu ruim"

class ErrorResponse(BaseModel):
    """ 
    Define como uma mensagem de erro será representada.
    """
    message: str = "Algo deu ruim"