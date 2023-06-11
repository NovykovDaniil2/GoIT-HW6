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
    contacts = await repository_contacts.get_birthday(days_range, db, current_user)
    return contacts


@cache
@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts


@cache
@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@cache
@router.post("/", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    return await repository_contacts.create_contact(body, db, current_user)


@cache
@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@cache
@router.delete("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(token_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact