from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import token_service
from src.conf.config import settings 


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=EmailStr(settings.mail_from),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Email service",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email_confirmation(email: EmailStr, username: str, host: str):
    """
    The send_email_confirmation function sends an email to the user with a link that they can click on
    to confirm their email address. The token_verification variable is used to create a JWT token for the
    user's email address, which will be sent in the confirmation link. The message variable contains all of
    the information needed for sending an HTML-formatted message using FastMail's send_message function.

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username of the user that is registering
    :param host: str: Create the link to the email confirmation page
    :return: A coroutine, which is a special type of object that can be used with
    :doc-author: Trelent
    """
    try:
        token_verification = await token_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)


async def send_email_reset(email: EmailStr, new_password: str):
    """
    The send_email_reset function sends an email to the user with a new password.
        Args:
            email (str): The user's email address.
            new_password (str): A randomly generated password for the user.

    :param email: EmailStr: Specify the email address of the user
    :param new_password: str: Pass the new password to the template
    :return: A coroutine object
    :doc-author: Trelent
    """
    try:
        message = MessageSchema(
            subject="Password reset",
            recipients=[email],
            template_body={"new_password": new_password},
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="password_reset.html")
    except ConnectionErrors as err:
        print(err)
