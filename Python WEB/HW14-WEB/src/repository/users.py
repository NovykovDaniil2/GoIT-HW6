from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Specify the email of the user we want to get from our database
    :param db: Session: Pass in the database session
    :return: The first user that matches the email address
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()
    

async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object to be created.
            db (Session): The SQLAlchemy session object used for querying the database.

    :param body: UserModel: Pass the usermodel object to the function
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        gr = Gravatar(body.email)
        avatar = gr.get_image()
    except Exception as err:
        print(err)
    new_user = User(**dict(body), avatar = avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Get the user's id
    :param token: str | None: Pass the token to the function
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Pass in the email address of the user to be confirmed
    :param db: Session: Pass in the database session
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that is being passed into the function
    :param db: Session: Pass the database session to the function
    :return: The updated user
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def change_password(user: User, new_password: str, db: Session) -> None:
    """
    The change_password function takes a user and new_password as arguments,
    and changes the password of the user to new_password.


    :param user: User: Specify the user whose password is being changed
    :param new_password: str: Pass the new password to the function
    :param db: Session: Pass the database session to the function
    :return: None, because it does not return anything
    :doc-author: Trelent
    """
    user.password = new_password
    db.commit()


