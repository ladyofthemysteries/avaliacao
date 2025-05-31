from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from repositorio_usuario import AuthDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(senha: str):
  hash = pwd_context.hash(senha)
  return hash


def verify_hash_password(senha: str, hash_password: str):
  return pwd_context.verify(senha, hash_password)

SECRET_KEY = "laisa"
ALGORITHM = "HS256"

def create_jwt_token(email: str):
  expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  data = {
    'sub': email,
    'exp': expire
  }

  token = jwt.encode(data, SECRET_KEY, ALGORITHM)

  return token


def is_valid_password(senha: str):
  '''
    Tamanho mínimo: 8 caracteres
    Conter números, letras minúsculas, 
    maiúsculas, caracter especiais
  '''
  if len(senha) < 8:
    return False
  if not contem_numero(senha):
    return False
  return True


def contem_numero(text: str):
  numeros = '1234567890'
  for caractere in text:
    if caractere in numeros:
      return True
  return False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

auth_dao = AuthDAO()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
  try:
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = data['sub']
    user = auth_dao.buscar_usuario_por_email(email)
    return user
  except:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Token inválido ou Expirado!'
    )