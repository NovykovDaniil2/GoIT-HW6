from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, user: User) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session, user: User) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contact_by_first_name(first_name: int, db: Session, user: User) -> Contact:
    return db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == user.id)).all()


async def get_contact_by_last_name(last_name: int, db: Session, user: User) -> Contact:
    return db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == user.id)).all()


async def get_contact_by_email(email: int, db: Session, user: User) -> Contact:
    return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).all()


async def get_birthday(days_range, db: Session, user: User) -> List[Contact]:
    start_date = datetime.today()
    end_date = start_date + timedelta(days=days_range)
    return db.query(Contact).filter(and_(Contact.birthday >= start_date, Contact.birthday <= end_date, Contact.user_id == user.id)).all()


async def create_contact(body: ContactModel, db: Session, user: User) -> Contact:
    contact = Contact(**dict(body), user_id = user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session, user: User) -> Contact | None:
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
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact