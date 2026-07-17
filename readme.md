# 🏦 API de Sistema Bancário - Padrão MVC

Esta é uma API robusta que simula as operações essenciais de um sistema bancário, desenvolvida com foco em segurança de transações, arquitetura limpa e testes automatizados.

## 🚀 Tecnologias Utilizadas

* **Python 3** - Linguagem base do projeto.
* **FastAPI** - Framework web moderno, rápido (alta performance) e de fácil utilização.
* **SQLite** - Banco de dados relacional leve (serverless) integrado diretamente ao projeto.
* **Pytest** - Framework de testes automatizados para garantir a qualidade do software.
* **Swagger UI** - Documentação interativa gerada automaticamente pelo FastAPI para testar as rotas.

---

## 🏛️ Arquitetura do Projeto (MVC)

O projeto foi estruturado seguindo o padrão de arquitetura **MVC (Model-View-Controller)** para garantir a separação de responsabilidades, facilidade de manutenção e segurança:

* **`main.py` (Controller/View):** Gerencia as rotas da API, recebe as requisições dos usuários e aplica as regras de negócio básicas (validação de valores negativos, senhas e saldo suficiente) usando princípios de *Early Return*.
* **`repository.py` (Model/Repository):** Responsável por toda a comunicação direta com o banco de dados SQLite. Ele executa as queries SQL (`SELECT`, `UPDATE`) e isola a lógica de persistência de dados.
* **`database.py`:** Configura a criação e conexão inicial do banco de dados SQLite.
* **`test_main.py`:** Contém a suite de testes automatizados executada pelo Pytest.

---

## 🧪 Testes Automatizados

O projeto conta com testes de integração e unitários que validam cenários críticos do sistema:
* Tentativa de saque com saldo insuficiente (Garante o bloqueio e retorno de erro).
* Validações de depósitos ou saques com valores negativos.
* Segurança de transferências.

Para rodar os testes, basta executar o comando abaixo no terminal:

```bash
pytest
```
🛠️ Como Executar o Projeto Localmente

Clone o repositório:

```
git clone https://github.com/igorrzao/banco-mvc-fastapi.git
cd banco-mvc-fastapi
```
Instale as dependências (FastAPI, Uvicorn, Pytest, HTTPX):

```
pip install fastapi uvicorn pytest httpx
```
Inicie o servidor de desenvolvimento:
```
uvicorn main:app --reload
```
Acesse a documentação interativa (Swagger):
Abra o seu navegador e acesse: http://127.0.0.1:8000/docs
