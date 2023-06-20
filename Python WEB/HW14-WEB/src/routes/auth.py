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
    """
    The generate_password function generates a random password of length 8 characters.
    The default value for the length parameter is 8, but it can be changed to any integer value.
    The function returns a string containing the generated password.

    :param length: int: Specify the length of the password
    :return: A string
    :doc-author: Trelent
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes a UserModel object as input, which is validated by pydantic.
        If the email address already exists in the database, an HTTP 409 error is raised.
        The password field of the UserModel object is hashed using Argon2 and stored in that form to ensure security.
        A new user record is created with this information and returned to the client.

    :param body: UserModel: Pass the user model to the function
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base url of the server
    :param db: Session: Get the database session
    :return: A dict with the user and a message
    :doc-author: Trelent
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = password_service.hash_password(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email_confirmation, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    The login function is used to authenticate a user.
        It takes the email and password of the user as input,
        checks if they are valid, and returns an access token
        that can be used for future requests.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Get the database session
    :return: A dict with the access_token and refresh_token
    :doc-author: Trelent
    """
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
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns a new access_token,
        refresh_token, and the type of token (bearer).

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Get the database session
    :return: A dictionary with the access_token, refresh_token and token type
    :doc-author: Trelent
    """
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
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        The function then checks if there is a user with that email in our database, and if not, returns an error message.
        If there is a user with that email in our database, we check whether their account has already been confirmed or not.
            If it has been confirmed already, we return another error message saying so; otherwise we update their account status to &quot;confirmed&quot;.

    :param token: str: Get the token from the url
    :param db: Session: Get the database session
    :return: A message to the user
    :doc-author: Trelent
    """
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
    """
    The request_email function is used to send an email confirmation link to the user's email address.
    The function takes in a RequestEmail object, which contains the user's email address. The function then checks if
    the user exists and if they have already confirmed their account. If not, it sends them an email with a confirmation
    link.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks
    :param request: Request: Get the base_url of the application
    :param db: Session: Get a database session
    :return: A message to the user
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email_confirmation, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.post('/reset_password', dependencies=[Depends(RateLimiter(times=1, seconds=60))])
async def reset_password(body: RequestEmail, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    The reset_password function takes a RequestEmail object as input, which contains an email address.
    It then checks if the user exists in the database and generates a new password for them.
    The new password is hashed and stored in the database, replacing their old one.
    An email containing their new password is sent to them via send_email_reset function.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param db: Session: Get the database session
    :return: A message that the password was changed and sent to the user's email
    :doc-author: Trelent
    """
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
    """
    The change_password function allows a user to change their password.
        The function takes in the current_password and new_password as parameters,
        and returns a message if the password was successfully changed.

    :param body: ChangePassword: Get the email, current_password and new_password from the request
    :param db: Session: Get the database session
    :return: A dictionary with a message
    :doc-author: Trelent
    """
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