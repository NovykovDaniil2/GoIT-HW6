from Address_Book_Handler import AddressBot, performer, get_handler as a_get_handler
from Note_Book_Handler import NoteBot, performer as n_performer, get_handler as n_get_handler
from Sort_Files import start_sorting
from Сalculator import start_calc
from Snake import start_snake
from GameGooseKiller.Game_goose import start_goose
from AI_helper import get_handler as ai_get_handler
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pathlib
import openai
import os

def goose():
    return start_goose()

def snake():
    return start_snake()

def calculator():
    return start_calc()

def folder_sorter():
    return start_sorting()

def AI_helper():
    AI_completer = WordCompleter(['generate image', 'ask question', 'exit'])
    print('\033[32mYou have entered the AI helper\033[0m')
    current_path = pathlib.Path(__file__).parent
    if not os.path.exists(os.path.join(current_path, 'api_key.txt')):
        with open(os.path.join(current_path, 'api_key.txt'), 'w+') as fd:
            fd.write(input('Enter an API key: '))
    try:
        with open(os.path.join(current_path, 'api_key.txt'), 'r') as fd:
            openai.organization = "org-Iv8GTRdlAKB6oppYyfYCKgc1"
            openai.api_key = fd.readline()
            openai.Model.list()
    except:
        print( '\033[031m API is not avaliable\033[0m' )
        exit()
    while True:
        action = prompt('Choose action:\n> generate image\n> ask question\n> exit\n>>> ', completer=AI_completer)
        if action == 'exit':
            break
        try:
            print(ai_get_handler(action).processing())
        except KeyError:
            print('\033[31mThere is no such command\033[0m')
    return '\033[32mThank you for using our ai helper!'


def address_book():
    address_container = AddressBot()
    address_container.book.load()
    address_book_completer = WordCompleter(['help', 'add', 'search', 'edit', 'delete', 'save', 'load', 'congratulate', 'show', 'exit'])
    print('\033[32mYou have entered the address book. Enter your command ("help" to get a description of the commands)')
    while True:
        action = prompt('>>> ', completer=address_book_completer)
        if action == 'exit': 
            break
        try:
            print(performer(a_get_handler(action), address_container))
        except KeyError:
            print('\033[31mThere is no such command\033[0m')
    return '\033[32mThank you for using our address book!'

def note_book():
    note_container = NoteBot()
    note_book_completer = WordCompleter(['help', 'add note', 'add date', 'show all', 'change note', 'delete note', 'search', 'show date', 'done', 'return', 'add tag', 'sort by tags', 'snake','exit'])
    print('\033[32mYou have entered the note book. Enter your command ("help" to get a description of the commands)')
    while True:
        action = prompt('>>> ', completer=note_book_completer)
        if action == 'exit':
            note_container.book.save()
            break
        try:
            print(n_performer(n_get_handler(action), note_container))
        except KeyError:
            print('\033[31mThere is no such command\033[0m')
    return '\033[32mThank you for using our address book!'


def run():

    print('''\033[34m  _____                                     _                                      _    _          _                       
 |  __ \                                   | |                                    | |  | |        | |                      
 | |__) |   ___   __      __   ___   _ __  | |__     ___    _   _   ___    ___    | |__| |   ___  | |  _ __     ___   _ __ 
 |  ___/   / _ \  \ \ /\ / /  / _ \ | '__| | '_ \   / _ \  | | | | / __|  / _ \   |  __  |  / _ \ | | | '_ \   / _ \ | '__|\033[33m
 | |      | (_) |  \ V  V /  |  __/ | |    | | | | | (_) | | |_| | \__ \ |  __/   | |  | | |  __/ | | | |_) | |  __/ | |   
 |_|       \___/    \_/\_/    \___| |_|    |_| |_|  \___/   \__,_| |___/  \___|   |_|  |_|  \___| |_| | .__/   \___| |_|   
                                                                                                      | |                  
                                                                                                      |_|                  \033[0m\n''')
    while True:
        main_completer = WordCompleter(['address book', 'note book', 'folder sorter', 'calculator', 'snake', 'goose', 'ai helper', 'exit'])
        main_action = prompt('''You are in the main menu! Please select the section you need.\n> address book\n> note book\n> folder sorter\n> calculator\n> snake\n> goose\n> ai helper (beta, internet only)\n> exit\n>>> ''', completer=main_completer)
        if main_action == 'exit':
            break
        handler = {'calculator' : calculator, 'folder sorter' : folder_sorter, 'address book' : address_book, 'note book' : note_book, 'snake' : snake, 'goose' : goose, 'ai helper' : AI_helper}
        try:
            print(handler[main_action]())
        except KeyError:
            print('\033[31mThere is no such command')

    print('\033[32mThank you for using our concole assistant\033[0m')

if __name__ == '__main__':
    run()