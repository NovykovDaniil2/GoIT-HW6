import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contact,
    get_contacts,
    get_contact_by_first_name,
    get_contact_by_last_name,
    get_contact_by_email,
    get_birthday,
    create_contact,
    update_contact,
    remove_contact
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    LIMIT = 10
    OFFSET = 0
    DAYS_RANGE = 10
    EMAIL_FOR_CHANGE = 'test@test.com'

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username = 'username', email='test@example.com', password = 'password')
        self.contact = Contact(id = 1, first_name = 'Test', last_name = 'Test', phone = '+380000000000', email = 'test@example.com', birthday = '2023-06-23', user_id = 1)

    async def test_get_contact(self):
        self.session.query().filter().first.return_value = self.contact
        result = await get_contact(self.contact.id, self.session, self.user)
        self.assertEqual(result.first_name, self.contact.first_name)

    async def test_get_contacts(self):
        self.session.query().filter().offset().limit().all.return_value = [self.contact]
        result = await get_contacts(self.OFFSET, self.LIMIT, self.session, self.user)
        self.assertEqual(result[0].first_name, self.contact.first_name)

    async def test_get_contact_by_first_name(self):
        self.session.query().filter().all.return_value = self.contact
        result = await get_contact_by_first_name(self.contact.first_name, self.session, self.user)
        self.assertEqual(result.first_name, self.contact.first_name)

    async def test_get_contact_by_last_name(self):
        self.session.query().filter().all.return_value = self.contact
        result = await get_contact_by_last_name(self.contact.last_name, self.session, self.user)
        self.assertEqual(result.first_name, self.contact.first_name)

    async def test_get_contact_by_email(self):
        self.session.query().filter().all.return_value = self.contact
        result = await get_contact_by_email(self.contact.last_name, self.session, self.user)
        self.assertEqual(result.first_name, self.contact.first_name)

    async def test_get_birthday(self):
        self.session.query().filter().all.return_value = [self.contact]
        result = await get_birthday(self.DAYS_RANGE, self.session, self.user)
        self.assertEqual(result[0].first_name, self.contact.first_name)

    async def test_create_contact(self):
        contact_model = ContactModel(
                                    first_name=self.contact.first_name,
                                    last_name=self.contact.last_name, 
                                    email=self.contact.email, 
                                    phone = self.contact.phone, 
                                    birthday = self.contact.birthday
                                    )
        result = await create_contact(contact_model, self.session, self.user)
        self.assertEqual(result.first_name, self.contact.first_name)

    async def test_update_contact(self):
        self.session.query().filter().first.return_value = self.contact
        updated_contact = self.contact
        updated_contact.email = self.EMAIL_FOR_CHANGE
        result = await update_contact(self.contact.id, updated_contact, self.session, self.user)
        self.assertEqual(result.email, self.EMAIL_FOR_CHANGE)

    async def test_remove_contact(self):
        self.session.query().filter().first.return_value = self.contact
        result = await remove_contact(self.contact.id, self.session, self.user)
        self.assertEqual(result, self.contact)
 
