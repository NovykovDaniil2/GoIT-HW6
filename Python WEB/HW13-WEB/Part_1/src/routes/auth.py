import random
import string

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail, ChangePassword
from src.repository import users as repository_users
from src.services.auth import password_service, token_service
from src.services.email import send_email_confirmation, send_email_reset


router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


def generate_password(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = password_service.hash_password(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email_confirmation, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not password_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    access_token = await token_service.create_access_token(data={"sub": user.email})
    refresh_token = await token_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await token_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await token_service.create_access_token(data={"sub": email})
    refresh_token = await token_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await token_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email', dependencies=[Depends(RateLimiter(times=1, seconds=60))])
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email_confirmation, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.post('/reset_password', dependencies=[Depends(RateLimiter(times=1, seconds=60))])
async def reset_password(body: RequestEmail, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        new_password = generate_password()
        hashed_new_password = password_service.hash_password(new_password)
        await repository_users.change_password(user, hashed_new_password, db)
        background_tasks.add_task(send_email_reset, user.email, new_password)
        return {"message": "Check your email with new password"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with such email wasn't found!")


@router.post('/change_password', dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def change_password(body: ChangePassword, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user: 
        if body.current_password == body.new_password:
           return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords are same") 
        if password_service.verify_password(body.current_password, user.password):
            hashed_new_password = password_service.hash_password(body.new_password)
            await repository_users.change_password(user, hashed_new_password, db)
            return {"message": "Your password has been successfully changed!"}
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with such email wasn't found!")