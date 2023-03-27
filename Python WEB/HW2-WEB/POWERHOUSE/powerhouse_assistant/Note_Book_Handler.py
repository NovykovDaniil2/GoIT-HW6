from Note import *
from abc import ABC, abstractmethod
import re
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt


class NoteBot:
    def __init__(self) -> None:
        self.book = NoteBook()


class Command(ABC):
    @abstractmethod
    def processing(self, note_instance: NoteBot):
        pass


class HelpMe(Command):
    def processing(self, note_instance: NoteBot):
        return note_instance.book.help_me()


class GoodBye(Command):
    def processing(self, note_instance: NoteBot):
        return note_instance.book.goodbye()


class AddNote(Command):
    def processing(self, note_instance: NoteBot):
        return note_instance.book.add_note(input("Note text: "))


class ShowAll(Command):
    def processing(self, note_instance: NoteBot):
        return note_instance.book.show_all()


class FindNote(Command):
    def processing(self, note_instance: NoteBot):
        subtext = input("Enter subtext to find contact: ")
        return note_instance.book.find_note(subtext)


class AddDate(Command):
    def processing(self, note_instance: NoteBot):
        id = int(prompt('Give an ID: ', validator=ValidateID()))
        date = prompt('Date (day-month-year): ', validator=ValidateDate())
        return note_instance.book.add_date(id, date)


class ChangeNote(Command):
    def processing(self, note_instance: NoteBot):
        id = int(prompt('Give an ID: ', validator = ValidateID()))
        return note_instance.book.change_note(id, input("Enter new note: "))


class DelNote(Command):
    def processing(self, note_instance: NoteBot):
        id = int(prompt('Give an ID: ', validator = ValidateID()))
        return note_instance.book.del_note(id)


class ShowDate(Command):
    def processing(self, note_instance: NoteBot):
        date = prompt('Date: ', validator = ValidateDate())
        days = int(prompt('Days range (optionally): ', validator = ValidateDays()))
        return note_instance.book.show_date(date, days)


class DoneNote(Command):
    def processing(self, note_instance: NoteBot):
        id = int(prompt('Give an ID: ', validator=ValidateID()))
        return note_instance.book.done_note(id)


class ReturnNote(Command):
    def processing(self, note_instance: NoteBot):
        id = int(prompt('Give an ID: ', validator=ValidateID()))
        return note_instance.book.return_note(id)


class AddTag(Command):
    def processing(self, note_instance: NoteBot):
        id = int(prompt('Give an ID: ', validator=ValidateID()))
        return note_instance.book.add_tag(id, input("Enter tags: "))


class SortByTags(Command):
    def processing(self, note_instance: NoteBot):
        return note_instance.book.sort_by_tags()

COMMANDS = {
    'help': HelpMe,
    'exit': GoodBye,
    'add note': AddNote,
    'add date': AddDate,
    'show all': ShowAll,
    "change note ": ChangeNote,
    "delete note ": DelNote,
    "search ": FindNote,
    "show date ": ShowDate,
    "done ": DoneNote,
    "return": ReturnNote,
    "add tag": AddTag,
    'sort by tags': SortByTags

}


class ValidateID(Validator):
    def validate(self, document) -> None:
        id = document.text
        if not id.isdigit():
            i = 0
            for i, c in enumerate(id):
                if not c.isdigit():
                    break
            raise ValidationError(message='ID should be an integer', cursor_position=i)


class ValidateDate(Validator):
    def validate(self, document) -> None:
        date = document.text
        if not re.match(r"\d{2}[-]\d{2}[-]\d{4}", date):
            raise ValidationError(message='Data should be in format day-month-year', cursor_position = 0)
        try:
            date_checker = date
            datetime.datetime.strptime(date_checker, '%d-%m-%Y')
        except:
            raise ValidationError(message='The date must be available', cursor_position = 0)
        

class ValidateDays(Validator):
    def validate(self, document) -> None:
        days = document.text
        if not days.isdigit():
            days = 0
            raise ValidationError(message='Days should be an integer', cursor_position = 0)  
        if int(days) > 366:
            raise ValidationError(message='Too big number (max 366)', cursor_position=0)


def get_handler(action):
    for command in COMMANDS.keys():
        if action in command:
            return COMMANDS[command]()


def performer(command: Command, note_instance: NoteBot):
    if command:
        return command.processing(note_instance)
    return '\033[31mThere is no such command'


