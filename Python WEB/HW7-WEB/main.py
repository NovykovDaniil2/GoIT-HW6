from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from src.operations import CRUD
from src.models import Teacher, Student, Subject, Grade, Group

INSTANCES = {
    "Teacher": Teacher,
    "Student": Student,
    "Grade": Grade,
    "Subject": Subject,
    "Group": Group,
}
table_completer = WordCompleter(["Teacher", "Student", "Grade", "Subject", "Group", "Exit"])
action_completer = WordCompleter(["create", "read", "update", "delete", "exit"])
crud_interface = CRUD()

print("\033[32mHi! I am your CRUD assistant!\033[0m")

while True:
    print(
        "\033[33mSelect the table you want to perform operations on: \n > Teacher \n > Student \n > Subject \n > Group \n > Grade \033[31m\n >> Exit\033[0m"
    )
    try:
        command = prompt(">>> ", completer=table_completer)
        if command == "Exit":
            print("\033[035mGood buy\033[0m")
            break
        table = INSTANCES[command]
        print(
            "\033[32mChoose an action: \n > create \n > read \n > update \n > delete \n \033[31m>> exit\033[0m"
        )
        action = prompt(">>> ", completer=action_completer)
        match action:
            case "create":
                print(crud_interface.add(table))
            case "read":
                print(crud_interface.show(table))
            case "update":
                print(crud_interface.update(table))
            case "delete":
                print(crud_interface.delete(table))
            case "exit":
                print("\033[035mGood buy\033[0m")
                break
            case _:
                print("\033[31mUnknown action!\033[0m")
    except KeyError:
        print("\033[31mUnknown table!\033[0m")
