import datetime
import pickle
import re
from collections import UserDict
from pathlib import Path
import logging
from prettytable import PrettyTable
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
import os

if not os.path.exists('note_saves'):
    os.mkdir('note_saves')
    with open('note_saves\\note_book.log', 'w+') as fd:
        pass
    with open('note_saves\\note_book_auto_save.bin', 'w+') as fd:
        pass

logger = logging.getLogger("nb_log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s]   %(message)s")
fh = logging.FileHandler("note_saves\\note_book.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)


N = 5  # number of notes per page


class DateIsNotValid(Exception):
    """You cannot add an invalid date"""


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __le__(self, other) -> bool:
        return self.value <= other.value

    def __ge__(self, other) -> bool:
        return self.value >= other.value


class ExecDate(Field):
    def __str__(self) -> str:
        if self.value is None:
            return " - "
        else:
            return f"{self.value:%d %b %Y}"

    @property
    def value(self) -> datetime.date:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                try:
                    self.__value = datetime.datetime.strptime(value, "%d-%m-%Y").date()
                except ValueError:
                    raise DateIsNotValid


class Tag(Field):
    def __str__(self) -> str:
        return f"{self.value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value


class Text(Field):
    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value:
            self.__value = value
        else:
            self.__value = "No text"
        print(self.__value)

    def __str__(self) -> str:
        return f"{self.value}"


class Note:
    def __init__(self, note_book, text: str) -> None:
        note_book.id_counter += 1
        self.id = note_book.id_counter
        self.is_done = False
        self.exec_date = None
        self.tags = []
        self.text = text

    def __str__(self):
        def hyphenation_string(text) -> str:
            result_list = re.findall(r".{50}", text)
            if result_list:
                result = ""
                for i in result_list:
                    if i[49] == " ":
                        result += i + "\n"
                    else:
                        result += i + "-" + "\n"
                result = result + text[len(result) - 2 :]
                return result
            else:
                result = text
                return result

        return (
            f"ID: {self.id:^10} {' ' * 17} Date: {self.exec_date}\n"
            f"Tags: {', '.join(self.tags)}\n"
            f"{hyphenation_string(self.text)}"
        )


class NoteBook(UserDict):
    id_counter = 0

    def __init__(self) -> None:
        super().__init__()
        logger.info('Note book has been created')
        self.filename = Path("note_saves\\note_book_auto_save.bin")
        if self.filename.exists():
            try:
                with open(self.filename, "rb") as db:
                    self.data = pickle.load(db)
            except:
                pass
        if len(self.data) > 0:
            self.id_counter = max(self.data.keys())

    def save(self):
        with open(self.filename, "wb") as db:
            pickle.dump(self.data, db)
            logger.info('Note book has been saved')

    def iterator(self, func=None, sort_by_tags=False):
        index, print_block = 1, "=" * 50 + "\n"
        is_empty = True
        data_values = self.data.values()
        if sort_by_tags:
            data_values = sorted(data_values, key=lambda x: x.tags)
        for note in data_values:
            if func is None or func(note):
                is_empty = False
                print_block += str(note) + "\n" + "-" * 50 + "\n"
                if index < N:
                    index += 1
                else:
                    yield print_block
                    index, print_block = 1, "=" * 50 + "\n"
        if is_empty:
            yield None
        else:
            yield print_block

    def add_note(self, note_text):
        note = Note(self, note_text)
        self[note.id] = note
        logger.info(f"Note ID:{note.id} added")
        self.save()
        return f"\033[32mNote ID:{note.id} added"

    def change_note(self, id_note: int, new_text: str):
        if not id_note in self.data:
            return '\033[31mThere is no note with such ID'
        self[id_note].text = new_text
        logger.info(f"Note ID:{id_note} changed")
        self.save()
        return f"\033[32mNote ID:{id_note} changed"

    def del_note(self, id_note: int):
        if not id_note in self.data:
            return '\033[31mThere is no note with such ID'
        agree_deny_compliter = WordCompleter(['yes', 'no'])
        yes_no = prompt(f"Are you sure you want to delete the note ID:{id_note}? (yes/not): ", completer=agree_deny_compliter)
        if yes_no == "yes":
            del self[id_note]
            logger.info(f"Note ID:{id_note} deleted")
            self.save()
            return f"\033[32mNote ID:{id_note} deleted"
        else:
            return "\033[31mNote hasn't been deleted!"

    def add_date(self, id_note: int, exec_date):
        if not id_note in self.data:
            return '\033[31mThere is no note with such ID'
        self[id_note].exec_date = ExecDate(exec_date)
        logger.info(f"Date {self[id_note].exec_date} added to note ID:{id_note}")
        self.save()
        return f"\033[32mDate {self[id_note].exec_date} added to note ID:{id_note}"

    def show_all(self, tag_sorted=False):
        def filter_func(note):
            return not note.is_done

        result = "List of all notes:\n"
        print_list = self.iterator(filter_func, tag_sorted)
        for item in print_list:
            if item is None:
                return "No notes found"
            else:
                result += f"{item}"
        return result

    def find_note(self, subtext: int):
        def filter_func(note):
            return subtext.lower() in note.text.lower()

        result = f'List of notes with text "{subtext}":\n'
        print_list = self.iterator(filter_func)

        for item in print_list:
            if item is None:
                return "No notes found"
            else:
                result += f"{item}"
        return result

    def show_date(self, date, days=0):
        def filter_func(note):
            if note.exec_date is None:
                return False
            date1 = (date_find.value - datetime.timedelta(days=days)).strftime(
                "%Y-%m-%d"
            )
            date2 = (date_find.value + datetime.timedelta(days=days)).strftime(
                "%Y-%m-%d"
            )
            return ExecDate(date1) <= note.exec_date <= ExecDate(date2)

        date_find = ExecDate(date)
        result = "List of notes with date:\n"
        print_list = self.iterator(filter_func)

        for item in print_list:
            if item is None:
                return "No notes found"
            else:
                result += f"{item}"
        return result

    def done_note(self, id_note):
        if not id_note in self.data:
            return '\033[31mThere is no note with such ID'
        if not self[id_note].is_done:
            self[id_note].is_done = True
            logger.info(f"Note ID: {id_note} marked as done")
            return f"\033[32mNote ID: {id_note} marked as done"
        else:
            return f"\033[31mNote ID: {id_note} is already done"

    def return_note(self, id_note):
        if not id_note in self.data:
            return '\033[31mThere is no note with such ID'
        if self[id_note].is_done:
            self[id_note].is_done = False
            logger.info(f"Note ID:{id_note} marked as not done")
            return f"\033[32mNote ID:{id_note} marked as not done"
        else:
            return f"\033[31mNote ID:{id_note} is not done"

    def add_tag(self, id_note, note_tags):
        if not id_note in self.data:
            return '\033[31mThere is no note with such ID'
        note_tags = re.sub(r"[;,.!?]", " ", note_tags).title().split()
        for tag in note_tags:
            if tag not in self[id_note].tags:
                self[id_note].tags.append(tag)
            else:
                note_tags.remove(tag)
            self[id_note].tags.sort(key=str.lower)
        if note_tags:
            logger.info(f'Tags {", ".join(sorted(note_tags))} added to note ID:{id_note}')
            self.save()
            return f'\033[32mTags {", ".join(sorted(note_tags))} added to note ID:{id_note}'
        else:
            return f"\033[31mNo tags added to note ID:{id_note}"

    def find_tag(self, tag):
        def filter_func(note):
            return tag.lower() in [t.lower() for t in note.tags]

        result = f'List of notes with tag "{tag}":\n'
        print_list = self.iterator(filter_func)
        for item in print_list:
            if item is None:
                return "\033[31mNo notes found"
            else:
                result += f"{item}"
        return result

    def sort_by_tags(self):
        return self.show_all(tag_sorted=True)

    def goodbye(self):
        self.save()
        print("\033[034mYou have finished working with self.\033[0m")
        logger.info('Note book has been closed')
        return "\033[033mGood buy!\033[0m"

    def help_me(self):
        note_book_docs = {
            'add note' : 'If you want to add note',
            'change note' : 'If you want to change note',
            'delete note' : 'If you want to delete note',
            'add date' : 'If you want to add/change date',
            'add tag' : ' If you want to add tag',
            'done' : 'If you want mark note as done',
            'return' : 'If you want mark note as not done',
            'show all' : 'If you want to show all notes',
            'show date' : 'If you want to show notes by date +- days',
            'find note' : 'If you want to find note by text',
            'find tag' : 'If you want to find note by tag',
            'sort by tags' : 'If you want to show all notes sorted by tags',


        }
        table = PrettyTable()
        table.field_names = ['Command', 'Description']
        for command, description in note_book_docs.items():
            table.add_row([command, description])
        return table