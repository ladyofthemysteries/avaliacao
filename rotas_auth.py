from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from repositorio_usuario import AuthDAO
from utils_auth import create_jwt_token, get_current_user, hash_password, is_valid_password, verify_hash_password
from modelos import SignIn, SignUp, Usuario

router = APIRouter()
auth_dao = AuthDAO()

@router.post('/auth/signin')
def login(usuario: SignIn):
    usuario_existente = auth_dao.buscar_usuario_por_email(usuario.email)

    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='E-mail ou senha incorreto')

    if not verify_hash_password(usuario.senha, usuario_existente.senha):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Email e/ou senha incorretos!')

    access_token = create_jwt_token(usuario_existente.email)
    
    return {
      'username': usuario_existente.username,
      'access_token': access_token}

@router.post('/auth/signup', status_code=status.HTTP_201_CREATED)
def signup(usuario: SignUp):
  usuario_existente = auth_dao.buscar_usuario_por_email(usuario.email)

  if not is_valid_password(usuario.senha):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'A senha não atende aos critérios.')

  if usuario_existente:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                        detail=f'Já existe um usuário com email {usuario.email}.')

  usuario.senha = hash_password(usuario.senha)
  usuario_salvo = auth_dao.criar_usuario(usuario)
  return usuario_salvo

@router.post('/auth/senhaesquecida')
def esquecer_senha(email):
  usuario = auth_dao.buscar_usuario_por_email(email)
  if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="E-mail não cadastrado."
        )
  reset_token = create_jwt_token(usuario.email, minutos_expiracao=5)
  return {
        "message": "Token de redefinição gerado. (simulado)",
        "reset_token": reset_token}

@router.get('/auth/me')
def me(user: Annotated[Usuario, Depends(get_current_user)]):
  return {
  "username": user.username,
  "email": user.email
}
