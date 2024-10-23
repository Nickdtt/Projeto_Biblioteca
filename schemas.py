from pydantic import BaseModel


class Usuario_Schema(BaseModel):

    id: int
    nome_usuario: str
    senha : str


class Livro_Schema(BaseModel):

    id: int
    nome_livro: str
    autor: str


class Token_Schema(BaseModel):
    access_token: str
    token_type: str