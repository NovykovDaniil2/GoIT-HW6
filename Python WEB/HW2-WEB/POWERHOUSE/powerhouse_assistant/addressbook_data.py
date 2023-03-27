import re
from abc import ABC, abstractmethod
import datetime
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt



class Field(ABC):
    @abstractmethod
    def __getitem__(self):
        pass


class Name(Field):
    def __init__(self):
        value = prompt("Name: ")
        self.value = value

    def __getitem__(self):
        return self.value


class Phone(Field):
    def __init__(self):
        self.value = prompt("Phone(-s) (correct format: +380.........): ", validator=ValidatePhone())

    def __getitem__(self):
        return (self.value,)


class Birthday(Field):
    def __init__(self):
        birthday = prompt('Birthday (DD-MM-YY): ', validator=ValidateBirthday())
        if not birthday:
            self.value = ''
        else:
            self.value = datetime.datetime.strptime(birthday, '%d-%m-%Y')

    def __getitem__(self):
        return self.value


class Email(Field):
    def __init__(self):
        self.value = prompt("Email: ", validator=ValidateEmail())

    def __getitem__(self):
        return self.value


class Address(Field):
    def __init__(self):
        value = input("Address: ")
        self.value = value

    def __getitem__(self):
        return self.value


class ValidatePhone(Validator):
    def validate(self, document) -> None:
        value_list = []
        value = document.text
        if not value:
            return ''
        if value.replace("+", "").isdigit():
            value = value.replace(" ", "").split("+")
        for phone in value[1:]:
            if re.match(r"[+380][0-9]{11}", phone):
                value_list.append("+" + phone)
            else:
                value_list.clear()
                raise ValidationError(message='Incorrect input! The correct number format is +380.........', cursor_position = 0)
        return ' '.join(value_list)


class ValidateEmail(Validator):
    def validate(self, document) -> None:
        email = document.text
        if not re.match(r"[A-Z|a-z][A-Z|a-z|0-9|_|.]{1,}@[a-z|A-Z|0-9|_]+\.[A-Za-z]{2,}", email) and not len(email) == 0:
            raise ValidationError(message='Incorrect email!', cursor_position = 0)
        else:
            return email
        

class ValidateBirthday(Validator):
    def validate(self, document) -> None:
        birth = document.text
        if not birth:
            return ''
        try:
            if not re.match(r'[0-9]{2}[-]{1}[0-9]{2}[-]{1}[0-9]{4}', birth):
                raise ValidationError(message='Incorrect format! You should enter birthday in format: day-month-year', cursor_position=0)
            date_checker = birth
            datetime.datetime.strptime(date_checker, '%d-%m-%Y')
        except:
            raise ValidationError(message='The date must be available', cursor_position = 0)





class Record:
    def __init__(self, name, phone="", address="", email="", birthday=""):
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email
        self.birthday = birthday
