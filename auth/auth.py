import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, TOKEN_EXPIRE_MINUTES
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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



def validar_token(token):

    try: 
        decode = jwt.decode(token, SECRET_KEY, algorithms="HS256")

    except jwt.exceptions.ExpiredSignatureError:
        return {"status":"erro", "motivo":"Token expirado."}
    
    except jwt.exceptions.InvalidTokenError:
        return {"status":"erro", "motivo":"Token inválido."}

    usuario = decode["sub"]

    return {"status":"sucesso", "sub":usuario}

    

def extrair_token(token: str = Depends(oauth2_scheme)):
    return token
