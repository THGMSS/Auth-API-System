from pydantic import BaseModel
from pydantic import Field

# Criando modelo de usuário
class User(BaseModel):
    username: str
    email: str
    password : str

# Criando modelo de token de atualização
class RefreshToken(BaseModel):
    refresh_token: str

# Criando modelo de reset de senha
class ResetPassword(BaseModel):
    new_password: str = Field(..., min_length=8)