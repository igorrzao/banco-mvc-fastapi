import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, TOKEN_EXPIRE_MINUTES



def criar_token(nomeUsuario:str):
        
    SECRET_KEY
    token = jwt.encode(
        {
            "sub":nomeUsuario,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        },
        SECRET_KEY,
        algorithm="HS256")

    return token