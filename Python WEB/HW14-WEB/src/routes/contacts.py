from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import redis
from redis_lru import RedisLRU

from src.database.db import get_db
from src.database.models import User
from src.services.auth import token_service
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
@router.get("/advanced_Search", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_contact(first_name: Optional[str] = None, last_name: Optional[str] = None, email: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The read_contact function will return a contact based on the first_name, last_name or email provided.
    If no contact is found, it will raise an HTTPException with status code 404 and detail &quot;Contact not found&quot;.


    :param first_name: Optional[str]: Tell the function that first_name is an optional parameter, and it should be a string
    :param last_name: Optional[str]: Specify that the last_name parameter is optional
    :param email: Optional[str]: Filter the contacts by email
    :param db: Session: Pass the database session to the function
    :param current_user: User: Check if the user is logged in
    :return: The contact with the specified first name, last name or email
    :doc-author: Trelent
    """
    contact = None
    if first_name:
        contact = await repository_contacts.get_contact_by_first_name(first_name, db, current_user)
    if last_name:
        contact = await repository_contacts.get_contact_by_last_name(last_name, db, current_user)
    if email:
        contact = await repository_contacts.get_contact_by_email(email, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@cache
@router.get("/birthday", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def get_nearest_birthday(days_range: Optional[int] = 7, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The get_nearest_birthday function returns a list of contacts with birthdays in the next 7 days.

    :param days_range: Optional[int]: Specify the number of days to look for birthdays
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user_id from the token
    :return: A list of contacts that have a birthday in the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthday(days_range, db, current_user)
    return contacts


@cache
@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip a number of contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository function
    :param current_user: User: Get the user's id
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts


@cache
@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The read_contact function is used to read a contact from the database.
    It takes in an integer representing the ID of the contact, and returns a Contact object.

    :param contact_id: int: Specify the contact id to be updated
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the token
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@cache
@router.post("/", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, which is validated by pydantic.
        The function also takes an optional db Session object and current_user User object as inputs,
            both of which are provided by dependency injection via FastAPI Depends() decorator.

    :param body: ContactModel: Define the type of data that will be passed to the function
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contact model object, which is the same as the body of the function
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db, current_user)


@cache
@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactModel object containing the new values for the contact.
            - contact_id: An integer representing the ID of an existing contact to be updated.
            - db (optional): A Session object used to connect to and query a PostgreSQL database, if not provided, one will be created using get_db().  This is done by passing get_db() as an argument into Depends(), which returns a callable that can then be passed into db as its default value.  This allows us to use dependency

    :param body: ContactModel: Get the contact information from the request body
    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the token
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@cache
@router.delete("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed, and returns a Contact object.

    :param contact_id: int: Specify the contact id of the contact we want to update
    :param db: Session: Pass the database session to the repository function
    :param current_user: User: Get the current user from the token
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact