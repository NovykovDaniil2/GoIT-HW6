from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings 


class Info:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET = settings.secret_key
    ALGORITHM = settings.algorithm


class Password(Info):
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        The verify_password function takes a plain-text password and a hashed password
        and returns True if the passwords match, False otherwise. The function uses the
        passlib library to verify that the hash matches what is stored in our database.

        :param self: Represent the instance of the class
        :param password: str: Store the password that is passed in from the user
        :param hashed_password: str: Pass in the hashed password from the database
        :return: A boolean value, true if the password is correct and false otherwise
        :doc-author: Trelent
        """
        return self.pwd_context.verify(password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        """
        The hash_password function takes a password as an argument and returns the hashed version of that password.
        The hash_password function uses the pwd_context object to generate a hash from the provided password.

        :param self: Represent the instance of the class
        :param password: str: Pass the password to be hashed
        :return: A string
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)
    

class Token(Info):

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        The create_access_token function creates a new access token for the user.
            Args:
                data (dict): A dictionary containing the user's information.
                expires_delta (Optional[float]): The time in hours until the token expires. Defaults to 10 hours if not specified.

        :param self: Refer to the class itself
        :param data: dict: Pass the data that will be encoded in the jwt
        :param expires_delta: Optional[float]: Set the time that the access token expires
        :return: A string that is the encoded access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(hours = expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(hours = 10)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope' : 'access_token'})
        encoded_access_token = jwt.encode(to_encode, self.SECRET, algorithm = self.ALGORITHM)
        return encoded_access_token
    
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None) -> str:
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): A dictionary containing the user's id and username.
                expires_delta (Optional[float]): The number of hours until the refresh token expires. Defaults to None, which sets it to 10 days from creation time.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the user's id, username and email
        :param expires_delta: Optional[float]: Set the expiry time of the token
        :return: A string
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(hours = expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days = 10)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope' : 'refresh_token'})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET, algorithm = self.ALGORITHM)
        return encoded_refresh_token
    
    async def decode_refresh_token(self, refresh_token: str) -> str:
        """
        The decode_refresh_token function is used to decode the refresh token.
        It takes a refresh_token as an argument and returns the email of the user who owns that token.
        If it fails, it raises an HTTPException with status code 401 (UNAUTHORIZED) and detail message 'Could not validate credentials'.


        :param self: Represent the instance of the class
        :param refresh_token: str: Pass in the refresh token
        :return: The email of the user who is trying to refresh their token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET, self.ALGORITHM)
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token as an argument and verifies it against
            our secret key. If the token is valid, we decode it to get its payload, which
            contains information about the user who made this request (such as their email).

        :param self: Represent the instance of a class
        :param token: str: Get the token from the request header
        :param db: Session: Get the database session
        :return: A user object, which is defined in the models
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},)
        try:
            payload = jwt.decode(token, self.SECRET, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as err:
            raise credentials_exception
        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user
    
    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function uses the jwt library to decode the token, which is then used to return the email address.

        :param self: Represent the instance of the class
        :param token: str: Pass in the token that is sent to the user's email
        :return: The email address of the user who is trying to verify their account
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")
        
    async def create_email_token(self, data: dict):
        """
        The create_email_token function takes a dictionary of data and returns a JWT token.
        The token is encoded with the SECRET key, which is stored in the .env file.
        The algorithm used to encode the token is also stored in the .env file.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data that needs to be encoded
        :return: A token, which is a string
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET, algorithm=self.ALGORITHM)
        return token
        
password_service = Password()
token_service = Token()