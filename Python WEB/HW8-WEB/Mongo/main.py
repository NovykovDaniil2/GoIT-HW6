from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from src.operations import help_, name, tag

COMMANDS = {'help': help_, 'name': name, 'tag': tag}
FUNC_ATTRS = {help_: [], name: ['Name'], tag: ['Tag']}
COMMAND_COMPLETER = WordCompleter(['help', 'name', 'tag', 'exit'])

print('\033[33mHi! I am MongoSearcher! (Enter to get a description)\033[0m')

while True:
    command = prompt('>>> ', completer = COMMAND_COMPLETER)
    if command == 'exit':
        print('\033[32mGood Bye!\033[0m')
        break
    if not command in COMMANDS:
        print('\033[31mUnknown command\033[0m')
        continue
    current_func = COMMANDS[command]
    attrs = [input(f'{attr.capitalize()}: ') for attr in FUNC_ATTRS[current_func]]
    print(COMMANDS[command](*attrs))