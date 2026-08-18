from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import inicializar_banco
from repository import verificar_credenciais, atualizar_saldo, buscar_saldo, buscar_usuario
from auth.auth import criar_token, validar_token, extrair_token, oauth2_scheme
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

inicializar_banco()

class ValorRecebido(BaseModel):
    valor: float

class TransferenciaRecebida(BaseModel):
    destinatario: str
    valor: float




@app.get("/saldo")
def verificar_saldo(token: str = Depends(oauth2_scheme)):

    resposta = validar_token(token)

    if resposta["status"] == "erro":
        return resposta

    usuario = resposta["sub"]

    resposta = buscar_saldo(usuario)

    if "status" in resposta and resposta["status"] == "erro":
        return resposta
    
    return {
            "status": "sucesso",
            "saldo_atual": resposta["saldo"]
            }

    

@app.post("/deposito")
def depositar(dados: ValorRecebido, token: str = Depends(oauth2_scheme)):

    resposta = validar_token(token)

    if resposta["status"] == "erro":
        return resposta

    valor_deposito = dados.valor

    if valor_deposito <= 0:
            return{"status":"erro", "mensagem": "Valor inserido inválido para depósito."}

    usuario = resposta["sub"]

    saldo_atual = buscar_saldo(usuario)

    if "status" in saldo_atual and saldo_atual["status"] == "erro":
            return saldo_atual

    novo_saldo = saldo_atual["saldo"] + valor_deposito

    atualizar_saldo(usuario, novo_saldo)

    return {
            "status": "sucesso",
            "mensagem": "Depósito realizado com sucesso!",
            "titular": usuario,
            "saldo_anterior": saldo_atual["saldo"],
            "novo_saldo": novo_saldo
        }


@app.post("/saque")
def sacar(dados: ValorRecebido, token: str = Depends(oauth2_scheme)):

    resposta = validar_token(token)

    if resposta["status"] == "erro":
        return resposta

    valor_saque = dados.valor

    if valor_saque <= 0:
        return{"status":"erro", "mensagem": "Valor inserido inválido para saque"}

    usuario = resposta["sub"]
 
    saldo_atual = buscar_saldo(usuario)

    if "status" in saldo_atual and saldo_atual["status"] == "erro":
        return saldo_atual

    if valor_saque > saldo_atual["saldo"]:
        return{"status":"erro", "mensagem":"O valor de saque deve ser menor ou igual que o saldo da conta."}

    novo_saldo = saldo_atual["saldo"] - valor_saque

    atualizar_saldo(usuario, novo_saldo)

    return {
            "status": "sucesso",
            "mensagem": "Saque realizado com sucesso!",
            "titular": usuario,
            "saldo_anterior": saldo_atual["saldo"],
            "novo_saldo": novo_saldo
    }
    

@app.post("/transferir")
def transferir(dados: TransferenciaRecebida, token: str = Depends(oauth2_scheme)):

    resposta = validar_token(token)

    if resposta["status"] == "erro":
        return resposta
    
    remetente = resposta["sub"]

    valor_transferencia = dados.valor
    
    if valor_transferencia <= 0:
        return{"status":"erro", "mensagem":"Valor inserido inválido para transferência"}

    destinatario = dados.destinatario

    if remetente == destinatario:
        return{"status":"erro", "mensagem":"O Remetente deve ser diferente do Destinatário!"}

    busca_destinatario = buscar_usuario(destinatario)

    if "status" in busca_destinatario and busca_destinatario["status"] == "erro":
        return busca_destinatario

    buscar_saldo_remetente = buscar_saldo(remetente)
    saldo_remetente = buscar_saldo_remetente["saldo"]

    if saldo_remetente < valor_transferencia:
        return{"status":"erro", "mensagem":"Saldo insuficiente para transferência"}

    buscar_saldo_destinatario = buscar_saldo(destinatario)
    saldo_destinatario = buscar_saldo_destinatario["saldo"]

    novo_saldo_remetente = saldo_remetente - valor_transferencia

    novo_saldo_destinatario = saldo_destinatario + valor_transferencia

    atualizar_saldo(remetente, novo_saldo_remetente)
    atualizar_saldo(destinatario, novo_saldo_destinatario)

    return{"status":"sucesso", "mensagem":"Transferência realizada com sucesso!"}

    


    




@app.post("/login")
def realizarLogin(dadosLogin: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    
    usuarioDigitado = dadosLogin.username
    senhaDigitada = dadosLogin.password
 
    resposta = verificar_credenciais(usuarioDigitado, senhaDigitada)

    if resposta["status"] == "erro":
        return resposta

    
    token = criar_token(usuarioDigitado)

    return {
        "status":"sucesso",
        "access_token": token,
        "token_type": "bearer"
    }