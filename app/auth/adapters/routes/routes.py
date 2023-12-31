from datetime import timedelta
from sqlalchemy import select
from dotenv import dotenv_values
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.adapters.exceptions.exceptions import UnauthorizedException
from app.infrastructure.database import ConectDatabase
from app.auth.domain.pydantic.userauth import TokenResponse, User
from app.auth.adapters.services.user import changePassword, createAccessToken, getCurrentActivateUser, oauth_2_scheme,  get_token_from_header,generateAccessTokenForRefreshToken, getCurrentUser, authenticateUser, createRefreshToken, recoveryPassword, confirmCode
from fastapi import Form
from typing import Annotated
from app.users.adapters.sqlalchemy.user import User as UserSql

auth = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)

session = ConectDatabase.getInstance()
values = dotenv_values('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = values.get('ACCESS_TOKEN_EXPIRE_MINUTES')


@auth.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticateUser(form_data.username, form_data.password)
    
    if not user:
        UnauthorizedException()

    access_token = createAccessToken({"sub": user.email})    

    return {
        "access_token": access_token,
        "user":  user
    }

@auth.post("/recover-password")
async def recovery_password(email: str):
    res = recoveryPassword(email)
    return res

@auth.post('/confirm-recover')
async def confirm_recover(code: str, email: str):
    res = confirmCode(code, email)
    return res

@auth.post('/change-password')
async def change_password(password: Annotated[str, Form()], apikey: str):
    user_changed = changePassword(password, apikey=apikey)
    return user_changed


@auth.get("/user/me")
async def get_current_user(user:User = Depends(getCurrentActivateUser)):
    userSQl:UserSql = session.scalars(select(UserSql).where(UserSql.email == user.email)).first()
    return {
        "id":userSQl.id,
        "name":userSQl.name,
        "document_type":userSQl.document_type,
        "document":userSQl.document,
        "phone":userSQl.phone,
        "email":userSQl.email,
        "status":userSQl.status,
        "role":userSQl.role.name,
        "permissions": user.permissions
    }