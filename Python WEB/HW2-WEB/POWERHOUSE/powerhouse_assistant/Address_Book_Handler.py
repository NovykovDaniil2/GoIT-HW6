from addressbook import *
from abc import abstractmethod, ABC
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter


class AddressBot:
    def __init__(self):
        self.book = AddressBook()


class Command(ABC):
    @abstractmethod
    def processing(self):
        pass


class Add(Command):
    def processing(self, data_container: AddressBot):
        name = Name().value.strip()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        address = Address().value
        record = Record(name, phones, birth, email, address)
        data_container.book.save()
        return data_container.book.add(record)


class Search(Command):
    def processing(self, data_container: AddressBot):
        category_completer = WordCompleter(['name', 'phone', 'email', 'address', 'birthday'])
        category = prompt('Enter a search category (name/phone/email/address/birthday) : ', completer=category_completer).lower().replace(" ", "")
        search_parameter = input("Enter the search parameter: ").lower().replace(" ", "")
        result = data_container.book.search(category, search_parameter)
        return result


class Edit(Command):
    def processing(self, data_container: AddressBot):
        category_completer = WordCompleter(['name', 'phone', 'email', 'address', 'birthday'])
        contact_data = input("Enter any data about contact that you want to change: ")
        new_category = prompt('Enter a category (name/phone/email/address/birthday) : ', completer=category_completer).lower().replace(" ", "")
        data_container.book.save()
        return data_container.book.edit(contact_data, new_category)


class Delete(Command):
    def processing(self, data_container: AddressBot):
        contact_info_to_remove = input("Enter any data about contact that you want to delete: ").strip().lower()
        data_container.book.save()
        return data_container.book.delete(contact_info_to_remove)


class Save(Command):
    def processing(self, data_container: AddressBot):
        return data_container.book.save()


class Load(Command):
    def processing(self, data_container: AddressBot):
        return data_container.book.load()


class Congratulate(Command):
    def processing(self, data_container: AddressBot):
        days_range = int(prompt('Enter the range of days: ', validator=ValidateDays()))
        return data_container.book.congratulate(days_range)



class Show(Command):
    def processing(self, data_container: AddressBot):
        return data_container.book.show()


class Help(Command):
    def processing(self, data_container: AddressBot):
        return data_container.book.help_me()
    

class ValidateDays(Validator):
    def validate(self, document) -> None:
        days = document.text
        if not days.isdigit():
            raise ValidationError(message='Days should be an integer', cursor_position=0)
        if int(days) > 366:
            raise ValidationError(message='Too big number (max 366)', cursor_position=0)
        return days

        


COMMANDS = {
    "help": Help,
    "add": Add,
    "search": Search,
    "edit": Edit,
    "delete": Delete,
    "save": Save,
    "load": Load,
    "congratulate": Congratulate,
    "show": Show,
}


def get_handler(action):
    for command in COMMANDS.keys():
        if action in command:
            return COMMANDS[command]()


def performer(command: Command, data_container: AddressBot):
    if command:
        return command.processing(data_container)
    return 'There is no such command'













