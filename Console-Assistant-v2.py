from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self.value = value
        
    def __str__(self) -> str:
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name: Name, phone: Phone) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

class AddressBook(UserDict):
    def add_record(self, record: Record) -> dict:
        self.data[record.name.value] = record
        return self.data

if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    
    print('All Ok)')