from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contact_by_first_name(first_name: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.first_name == first_name).all()


async def get_contact_by_last_name(last_name: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.last_name == last_name).all()


async def get_contact_by_email(email: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.email == email).all()


async def get_birthday(days_range, db: Session) -> List[Contact]:
    start_date = datetime.today()
    end_date = start_date + timedelta(days=days_range)
    return db.query(Contact).filter(Contact.birthday >= start_date, Contact.birthday <= end_date).all()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name = body.first_name, last_name = body.last_name, email = body.email, phone = body.phone, birthday = body.birthday, additional = body.additional)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact