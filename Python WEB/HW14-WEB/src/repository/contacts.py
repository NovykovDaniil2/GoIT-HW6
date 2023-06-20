from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, user: User) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param skip: int: Skip a number of contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass in the database session
    :param user: User: Get the contacts of a specific user
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session, user: User) -> Contact:
    """
    The get_contact function takes in a contact_id and returns the corresponding Contact object.
        Args:
            contact_id (int): The id of the Contact to be retrieved.
            db (Session): A database session for querying Contacts from the database.
            user (User): The User who owns this Contact.

    :param contact_id: int: Specify the contact to be retrieved
    :param db: Session: Pass the database session to the function
    :param user: User: Make sure that the user is getting their own contact
    :return: A contact object
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contact_by_first_name(first_name: int, db: Session, user: User) -> Contact:
    """
    The get_contact_by_first_name function returns a contact by first name.

    :param first_name: int: Specify the first name of the contact to be retrieved
    :param db: Session: Pass the database session to the function
    :param user: User: Make sure that the user is only able to get contacts that they have created
    :return: A list of contacts with the given first name
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == user.id)).all()


async def get_contact_by_last_name(last_name: int, db: Session, user: User) -> Contact:
    """
    The get_contact_by_last_name function returns a list of contacts with the given last name.


    :param last_name: int: Filter the database query by last name
    :param db: Session: Access the database
    :param user: User: Check if the user is authorized to access this function
    :return: A list of contacts with the same last name
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == user.id)).all()


async def get_contact_by_email(email: int, db: Session, user: User) -> Contact:
    """
    The get_contact_by_email function takes in an email and a database session,
    and returns the contact with that email. If no such contact exists, it raises a 404 error.

    :param email: int: Filter the database by email
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user's id from the database
    :return: A list of contacts with the specified email address
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).all()


async def get_birthday(days_range, db: Session, user: User) -> List[Contact]:
    """
    The get_birthday function returns a list of contacts whose birthday is within the specified range.
        Args:
            days_range (int): The number of days from today to search for birthdays.
            db (Session): A database session object used to query the database.
            user (User): The user who owns the contacts being queried.

    :param days_range: Determine the range of days to search for birthdays
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user id of the current user
    :return: A list of contacts that have a birthday in the next n days
    :doc-author: Trelent
    """
    start_date = datetime.today()
    end_date = start_date + timedelta(days=days_range)
    return db.query(Contact).filter(and_(Contact.birthday >= start_date, Contact.birthday <= end_date, Contact.user_id == user.id)).all()


async def create_contact(body: ContactModel, db: Session, user: User) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Deserialize the request body into a contactmodel object
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user id from the token
    :return: The contact that was created
    :doc-author: Trelent
    """
    contact = Contact(**dict(body), user_id = user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session, user: User) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified contact.

    :param contact_id: int: Identify the contact that will be deleted
    :param body: ContactModel: Get the data from the request body
    :param db: Session: Access the database
    :param user: User: Get the user id from the token
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User)  -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.
            user (User): The user who is removing this contact.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is authorized to delete a contact
    :return: A contact object or none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact