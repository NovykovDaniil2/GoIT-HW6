import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
    change_password,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    TEST_TOKEN = 'Bearer token'
    TEST_AVATAR = 'Link to the avatar'
    TEST_PASSWORD = 'Password'

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username = 'username', email='test@example.com', password = 'password')

    async def test_get_user_by_email(self):
        self.session.query.return_value.filter.return_value.first.return_value = self.user
        result = await get_user_by_email("test@example.com", self.session)
        self.assertEqual(result, self.user)

    async def test_create_user(self):
        new_user_model = UserModel(username = self.user.username, email = self.user.email, password = self.user.password)
        new_user = await create_user(new_user_model, self.session)
        self.assertEqual(new_user.username, self.user.username)

    async def test_update_token(self):
        result = await update_token(self.user, self.TEST_TOKEN, self.session)
        self.assertEqual(result, None)

    async def test_confirmed_email(self):
        result = await confirmed_email(self.user.email, self.session)
        self.assertEqual(result, None)

    async def test_update_avatar(self):
        result = await update_avatar(self.user.email, self.TEST_AVATAR, self.session)
        self.assertEqual(result.avatar, self.TEST_AVATAR)

    async def test_change_password(self):
        result = await change_password(self.user, self.TEST_PASSWORD, self.session)
        self.assertEqual(result, None)