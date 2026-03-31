from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer as oapb, OAuth2PasswordRequestForm
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import schema

# Cria todas as tabelas do banco de dados
models.Base.metadata.create_all(bind=engine)

# Criar sessão no banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

SECRET_KEY = 'segredo_super_forte'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30  # 30 dias

# Segurança pra senha, pois sempre salvamos criptografada (hash)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash: str):
    return pwd_context.verify(senha, hash)

@router.post('/register')
def register(user: schema.User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail='Usuário já existe')

    new_user = models.User(username=user.username, email=user.email, hashed_password=hash_senha(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'Msg': 'Usuário criado com sucesso'}

def create_token(data: dict):
    dados = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados.update({'exp': expire})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    dados = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    dados.update({'exp': expire})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    refresh_token = create_refresh_token({"sub": db_user.username}) if db_user else None
    username = db.query(models.User).filter(models.User.username == form_data.username).first()
    if username:
        raise HTTPException(status_code=400, detail='Por favor, use o email para login!')

    if not db_user:
        raise HTTPException(status_code=400, detail='Usuário não existe')

    if not verificar_senha(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Senha incorreta')

    token = create_token({'sub': db_user.username})

    return {'access_token': token, 
            'token_type': 'bearer',
            'refresh_token': refresh_token}

oauth2_scheme = oapb(tokenUrl='/login')

def get_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return user  # Return user object instead of username for full context

@router.get('/get-user')
def get_user(user: models.User = Depends(get_user_from_token)):
    # Agora user é um objeto User e não string
    return {'msg': f'Olá {user.username}, voce está autenticado'}

@router.post('/refresh-token')
def refresh_token(refresh_token: schema.RefreshToken):
    try:
        payload = jwt.decode(refresh_token.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Refresh token_invalido')
        new_token = create_refresh_token({'sub': username})
        return {'access_token': new_token, 'token_type': 'bearer'}
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')

@router.put('/update-password')
def update_password(new_password: schema.ResetPassword, db: Session = Depends(get_db), user: models.User = Depends(get_user_from_token)):
    try:
        user.hashed_password = hash_senha(new_password.new_password)
        db.commit()
        db.refresh(user)
        return {'msg': 'Senha atualizada com sucesso'}
    except Exception as e:
        print('Erro ao atualizar a senha: ', e)

