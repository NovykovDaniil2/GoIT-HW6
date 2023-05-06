import json
from collections import deque
from mongoengine import Document
from os.path import exists

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt

from src.models import Authors, Quotes
import src.connect


INSTANCES = {"Authors": Authors, "Quotes": Quotes}


def spread_tasks(filename: str) -> deque:
    queue = deque()
    with open(filename, "r") as fd:
        data = json.load(fd)
        for value in data:
            queue.append(value)
    return queue


def add_author(queue: deque, table: Document) -> None:
    for _ in range(len(queue)):
        task = queue.pop()
        record = table(
            fullname=task["fullname"],
            born_date=task["born_date"],
            born_location=task["born_location"],
            description=task["description"],
        )
        record.save()


def add_quotes(queue: deque, table: Document) -> None:
    for _ in range(len(queue)):
        task = queue.pop()
        author = Authors.objects(fullname=task["author"]).first()
        if author:
            record = table(
                tags=task["tags"],
                author=str(author.id),
                quote=task["quote"],
            )
            record.save()

def main():

    print("\033[1mChoose file category that you want to add \n> Authors \n> Quotes\033[0m")

    category_completer = WordCompleter(["Authors", "Quotes"])
    category = prompt(">>> ", completer=category_completer)
    if category not in ["Authors", "Quotes"]:
        return "\033[31mUnknown category\033[0m"
    
    filename = input("\033[1mFilename: \033[0m")
    if not exists(filename):
        return "\033[31mFile does not exist\033[0m"
    
    queue = spread_tasks(filename)

    match category:
        case 'Authors':
            add_author(queue, INSTANCES[category])
        case 'Quotes':
            add_quotes(queue, INSTANCES[category])

    return "\033[32mData was recorded successfully\033[0m"


if __name__ == "__main__":
    print(main())
