# 📖 Documentação da API de Autenticação (FastAPI)

Esta API implementa um sistema simples de autenticação utilizando JWT, oferecendo:

- Registro de usuários
- Login
- Refresh Token
- Proteção de rotas autenticadas
- Update_password

---

## 📚 Documentação Interativa

Acesse a documentação diretamente em: Ctrl + click
- [Swagger](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)
- [Se preferir o Postman] (https://www.postman.com/downloads/)
- [Se preferir o Insomnia] (https://insomnia.rest/download)

---

## 🔐 Autenticação

- **JWT (JSON Web Token):**
  - **Access Token:** expira em 15 minutos; utilize para acessar rotas protegidas.
  - **Refresh Token:** permite gerar novos access tokens após expiração.

---

## 📌 Endpoints

### 📝 Registro de Usuário

- **POST** `/register`
- **Exemplo de body (JSON):**
  ```json
  {
    "username": "Daniel",
    "email": "daniel@outlook.com",
    "password": "123456"
  }
  ```

### 🔓 Login

- **POST** `/login`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Parâmetros:**
  ```
  username=daniel@outlook.com
  password=123456
  ```

### ♻️ Refresh Token

- **POST** `/refresh-token`
- **Body (JSON):**
  ```json
  {
    "refresh_token": "SEU_REFRESH_TOKEN"
  }
  ```

### 👤 Usuário Autenticado

- **GET** `/get-user`
- **Headers:**
  ```
  Authorization: Bearer SEU_ACCESS_TOKEN
  ```

---

## 🔄 Atualizar senha

- **PUT** `/update-password`
### 🔐 Autenticação
É necessário enviar o token JWT no header:
Authorization: Bearer(seu token)
- **Body (JSON):**
```json
{
  "new_password": "sua_senha_nova" 
}
```


---

## 🧠 Explicando de forma simples

👉 Você está dizendo:

> “Só pode atualizar senha quem estiver logado”

E o jeito da API saber isso é:

👉 olhando o **Authorization header**

---

## 🚀 Dica nível profissional

Se quiser deixar mais bonito ainda:

```md
### 🔐 Header obrigatório

| Campo        | Valor                  |
|-------------|-----------------------|
| Authorization | Bearer {token}       |



## ⚙️ Como rodar o projeto

No terminal:
```
uvicorn main:app --reload
```

--------