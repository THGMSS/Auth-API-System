🚀 API de Autenticação (FastAPI) 

Bem-vindo! Esta API oferece autenticação baseada em JWT, permitindo registro, login, refresh de tokens e proteção de rotas.

---

## 📑 Rotas e Exemplos de Uso

### 👤 Registro de Usuário

- **Endpoint:** `POST /register`
- **Exemplo de corpo da requisição (JSON):**
  ```json
  {
    "username": "Daniel",
    "email": "daniel@gmail.com",
    "password": "1234"
  }
  ```

---

### 🔓 Login

- **Endpoint:** `POST /login`
- **Exemplo de corpo da requisição (x-www-form-urlencoded ou JSON):**
  ```json
  {
    "username": "daniel@gmail.com",
    "password": "1234"
  }
  ```

---

### ♻️ Refresh Token

- **Endpoint:** `POST /refresh-token`
- **Exemplo de corpo da requisição (JSON):**
  ```json
  {
    "refresh_token": "refresh_token_gerado_no_login"
  }
  ```

---

### 🔐 Acesso a Rotas Protegidas

- **Endpoint:** `GET /get-user`
- **Cabeçalho necessário:**
  ```
  Authorization: Bearer <access_token_gerado_no_login>
  ```

---

## 🛡️ Sobre Tokens

- **Access Token:** expira em 15 minutos.
- **Refresh Token:** expira em 30 dias; utilize para obter novos access tokens.

---

## 🌐 Documentação Interativa

- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

---

## ⚙️ Executando o Projeto

No terminal, rode:
```
uvicorn main:app --reload
```

---
Caso tenha dúvidas, consulte os exemplos acima ou utilize o Swagger para testar suas requisições.