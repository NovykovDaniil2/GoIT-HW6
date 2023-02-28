from collections import UserDict
import datetime
import json
import os

class Field:
    def __init__(self) -> None:
        self.__value = None

    def __str__(self) -> str:
        return str(self.__value)
    
class Name(Field):

    def get_value(self):
        return self.__value
    
    def value(self, new_value):
        self.__value = Name(new_value)

class Phone(Field):
    
    @property
    def value(self):
        try:
            return self.__value
        except AttributeError:
            print('Incorrect phone number format! Example of correct input: +380xxxxxxxxxx')

    #Checking user input
    @value.setter
    def value(self , new_value):
        checker = 0
        for i in new_value.split(' '):
            if len(i) != 13 or not i.startswith('+380') or not i[1:].isdigit() :
                continue
            else:
                checker += 1
        if len(new_value.split(' ')) == checker:
            self.__value = new_value.split()

class Birthday(Field):

    @property
    def value(self):
        return self.__value

    #Checking user input
    @value.setter
    def value(self, new_value):
        try:
            self.__value = datetime.datetime.strptime(str(new_value), '%Y-%m-%d')
        except:
            print(f"The date of birth was not specified or entered incorrectly. Correct format: {datetime.datetime.today().strftime('%Y-%m-%d')}")


class Record:
    def __init__(self, name: Name, phone: Phone , birthday: Birthday = None) -> None:
        self.name = name
        self.phones = phone
        if type(birthday) != None:
            self.birthday = birthday
    
    #A method that calculates the number of days until the next birthday
    def days_to_birthday(self) -> str:
        self.birthday = datetime.datetime.strptime(str(self.birthday), '%Y-%m-%d %H:%M:%S')
        if self.birthday > datetime.datetime.today():
            delta = self.birthday - datetime.datetime.today()
            print(f'The birthday will be in {delta.days} days')
        else:
            days_between_dates = 365 * (int(datetime.datetime.today().year) - int(self.birthday.year)) 
            self.birthday += datetime.timedelta(days = days_between_dates)
            delta = int((self.birthday - datetime.datetime.today()).days) 
            print(f'The birthday will be in {delta} days')

class AddressBook(UserDict):

    #A method that writes contacts to a contact book
    def add_record(self, record: Record) -> dict:
        if record.birthday == None:
            self.data[record.name] = record.phones
        elif record.phones == None:
            self.data[record.name] = f"You have entered an incorrect number! Example: +380*********    {record.birthday.strftime('%Y-%m-%d')}"
        else:
            self.data[record.name] = f"{record.phones}    {record.birthday.strftime('%Y-%m-%d')}"
        return self.data

    #A method that returns a generator based on contact book entries. n - the number of output contacts in one iteration.
    def iterator(self, n = 1):
        count = 0
        while count < len(self.data):
            yield {k: v for (k, v) in list(self.data.items())[count:count + n]}
            count += n

    #A method that saves contacts to JSON file
    def save_contact(self, record: Record) -> dict:

        #File creating
        try:
            with open('AddressBook.json', 'x') as fp:
                pass
        except:
            pass

        #Data parsing from JSON file
        with open('AddressBook.json', 'r') as file_r:
            try:
                current_contacts = json.load(file_r)
            except:
                current_contacts = []

        #Updating data from JSON file
        if record.birthday == None:
            current_contacts.append({'name' : record.name, 'phone' : record.phones})
        elif record.phones == None:
            current_contacts.append({'name' : record.name, 'phone' : "You have entered an incorrect number! Example: +380*********"})
        else:
            current_contacts.append({'name' : record.name, 'phones' : record.phones, 'birthday' : record.birthday.strftime('%Y-%m-%d')})
            
        #Overwriting updated data to JSON file
        with open('AddressBook.json', 'w', encoding = 'utf-8') as file_w:
            json.dump(current_contacts, file_w, indent = 2, ensure_ascii = False)

    #A method that will help you find the right contact in a JSON file
    def seek_contact(self, user_string: str):
        result_list = []
        with open('AddressBook.json', 'r', encoding = 'utf-8') as file_r:
            contacts = json.load(file_r)
        for contact in contacts:
            for elem in contact.values():
                if user_string in elem:
                    result_list.append(contact)
                elif isinstance(elem, list):
                    for i in elem:
                        if user_string in i:
                            result_list.append(contact)
        print(result_list)
