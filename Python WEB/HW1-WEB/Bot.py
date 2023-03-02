from AddressBook import *
from abc import abstractmethod, ABC


class Bot:

    def __init__(self):
        self.book = AddressBook()


class Command(ABC):

    @abstractmethod
    def processing(self):
        pass


class Add(Command):

    def processing(self, data_container: AddressBook):
        name = Name(input("Name: ")).value.strip()
        phones = Phone().value
        birth = Birthday().value
        email = Email().value.strip()
        status = Status().value.strip()
        note = Note(input("Note: ")).value
        record = Record(name, phones, birth, email, status, note)
        data_container.book.save('auto_save')
        return data_container.book.add(record)
    

class Search(Command):

    def processing(self, data_container: AddressBook):
        print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
        category = input('Search category: ')
        pattern = input('Search pattern: ')
        result = data_container.book.search(pattern, category)
        for account in result:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
                result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                print(result)


class Edit(Command):
    
    def processing(self, data_container: AddressBook):
        contact_name = input('Contact name: ')
        parameter = input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
        new_value = input("New Value: ")
        data_container.book.save('auto_save')
        return data_container.book.edit(contact_name, parameter, new_value)


class Remove(Command):
    
    def processing(self, data_container: AddressBook):
        pattern = input("Remove (contact name or phone): ")
        data_container.book.save('auto_save')
        return data_container.book.remove(pattern)


class Save(Command):

    def processing(self, data_container: AddressBook):
        file_name = input("File name: ")
        return data_container.book.save(file_name)


class Load(Command):

    def processing(self, data_container: AddressBook):
        file_name = input("File name: ")
        return data_container.book.load(file_name)


class Congratulate(Command):

    def processing(self, data_container: AddressBook):
        print(data_container.book.congratulate())


class View(Command):

    def processing(self, data_container: AddressBook):
        print(data_container.book)


class Help(Command):

    def processing(self, data_container: AddressBook):
        format_str = str('|{:%s%d}|' % ('^',20))
        for command in COMMANDS.keys():
            print(format_str.format(command))

    
COMMANDS = {
    'add' : Add(),
    'search' : Search(),
    'edit' : Edit(),
    'remove' : Remove(),
    'save' : Save(),
    'load' : Load(),
    'congratulate' : Congratulate(),
    'view' : View(),
    'help' : Help()
}

def get_handler(action):
    return COMMANDS[action]

def performer(command: Command, data_container: AddressBook):
    command.processing(data_container)

