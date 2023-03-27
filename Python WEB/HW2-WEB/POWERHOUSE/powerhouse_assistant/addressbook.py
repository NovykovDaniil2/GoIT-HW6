import datetime
import pickle
import logging
import os
from prettytable import PrettyTable
from addressbook_data import *

if not os.path.exists('address_saves'):
    os.mkdir('address_saves')
    with open('address_saves\\address_book.log', 'w+') as fd:
        pass
    with open('address_saves\\address_book_auto_save.bin', 'w+') as fd:
        pass

logger = logging.getLogger("ab_log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s]   %(message)s")
fh = logging.FileHandler("address_saves\\address_book.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)


class AddressBook:
    def __init__(self):
        self.data = []
        logger.info("Address book has been created")

    def add(self, record):
        self.data.append(
            {
                "Name": record.name,
                "Phone": record.phone,
                "Address": record.birthday,
                "Email": record.email,
                "Birthday": record.address,
            }
        )
        logger.info("The contact has been recorded successfully")
        return "\033[32mThe contact has been recorded successfully"

    def save(self):
        with open('address_saves\\address_book_auto_save.bin', "wb") as fd:
            pickle.dump(self.data, fd)
            logger.info(f"Address Book has been saved")
            return f"\033[32mAddress Book has been saved"

    def load(self):
        with open('address_saves\\address_book_auto_save.bin', "rb") as fd:
            if not os.stat('address_saves\\address_book_auto_save.bin').st_size == 0:
                self.data = pickle.load(fd)
                logger.info(f"Address Book has been loaded")
                return f"\033[32mAddress Book has been loaded from auto save file"
            logger.info(f"File to load is empty")
            return "\033[31mFile to restore is empty"

    @staticmethod
    def table_filler(table, contact):
        table.field_names = ["Name", "Phone", "Address", "Email", "Birthday"]
        phone_to_show = (
            " +".join(contact["Phone"].split("+")) if contact["Phone"] else ""
        )
        birthday_to_show = (
            contact["Birthday"].date()
            if not isinstance(contact["Birthday"], str)
            else contact["Birthday"]
        )
        table.add_row(
            [
                contact["Name"],
                phone_to_show,
                contact["Address"],
                contact["Email"],
                birthday_to_show,
            ]
        )

    def show(self):
        table = PrettyTable()
        if self.data:
            for contact in self.data:
                self.table_filler(table, contact)
            return table
        return '\033[31mThere is no contact'

    def edit(self, contact_data, new_category):
        category_container = {
            "Name": Name,
            "Phone": Phone,
            "Email": Email,
            "Address": Address,
            "Birthday": Birthday,
        }
        result = [
            contact
            for contact in self.data
            for val in contact.values()
            if str(contact_data).lower().strip() in str(val).lower().strip()
        ]
        if not result:
            return "\033[31mThere is no such contact"
        try:
            if new_category not in category_container.keys():
                raise ValueError
            else:
                result[0][new_category] = category_container[new_category]().value
                current_contact_name = result[0]["Name"]
                logger.info(f"Contact {current_contact_name} has been edited and saved to the auto save file ")
                return f"\033[32mContact {current_contact_name} has been edited "
        except ValueError:
            return "\033[31mThere is no such category"

    def delete(self, contact_info_to_remove):
        try:
            contact_to_remove = [
                i
                for i in self.data
                for info in i.values()
                if contact_info_to_remove in str(info).strip().lower()
            ]
            self.data.remove(contact_to_remove[0])
            current_contact_name = contact_to_remove[0]["Name"]
            self.save()
            logger.info(f"Contact {current_contact_name} has been deleted")
            return f"\033[32mContact {current_contact_name} has been deleted"
        except IndexError:
            return "\033[31mThere is no such contact!"

    def search(self, category, search_parameter):
        matching_contacts = []
        available_categories = [
            "name",
            "phone",
            "email",
            "address",
            "birthday",
        ]
        if category not in available_categories:
            return "\033[31mThere is no such category"
        for contact in self.data:
            if search_parameter in contact[category.capitalize()].lower():
                matching_contacts.append(contact)

        if matching_contacts:
            table = PrettyTable()
            for contact in matching_contacts:
                self.table_filler(table, contact)
        else:
            return '\033[31mThere is no such contact'
        return table

    def congratulate(self, days_range):
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        stop_date = start_date + datetime.timedelta(days=days_range)
        congratulate_dict = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": [],
        }
        for contact in self.data:
            if contact["Birthday"]:
                if contact["Birthday"] > stop_date:
                    continue
                current_birthday = contact["Birthday"].replace(year=datetime.datetime.now().year)
                if current_birthday < start_date:
                    current_birthday += datetime.timedelta(days=365)
                if start_date < current_birthday < stop_date:
                    congratulate_dict[current_birthday.strftime("%A")].append(contact["Name"])

        table = PrettyTable()
        table.field_names = ['Weekday', 'Сelebrants']
        for weekday, celebrants in congratulate_dict.items():
            table.add_row([weekday, ' '.join(celebrants)])
        return table
    
    def help_me(self):
        address_book_docs = {
            'add' : 'add contact',
            'search' : 'search contact using any information',
            'edit' : 'edit recorded contact',
            'delete' : 'delete existing contact',
            'save' : 'save your contact book to the file',
            'load' : 'recover contacts from the auto save file',
            'congratulate' : 'find out who you need to congratulate in the near future',
            'show' : 'print all contacts that you have',
            'exit' : 'to back to the main menu'
        }
        table = PrettyTable()
        table.field_names = ['Command', 'Description']
        for command, description in address_book_docs.items():
            table.add_row([command, description])
        return table