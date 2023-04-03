from threading import Thread, RLock
from queue import Queue
from pathlib import Path
import shutil
import os
from time import time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


EXTENDS = {
    'images' : (".png", ".jpeg", ".jpg", ".svg"),
    'videos' : (".avi", ".mp4", ".mov", ".mkv"),
    'documents' : (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"),
    'audios': (".mp3", ".ogg", ".wav", ".amr"),
    'archives': (".zip", ".tar", ".gz"),
    }


def create_basic_folders(path: Path):
    for key in EXTENDS.keys():
        if not os.path.exists(Path.joinpath(path, key)):
            os.mkdir(Path.joinpath(path, key))


def remove_empty_folders(path: Path):
    for elem in path.iterdir():
        if elem.is_dir() and os.listdir(elem) and os.path.basename(elem) not in EXTENDS.keys():
            th = Thread(target=remove_empty_folders, args=(elem, ))
            th.start()
            th.join()
        elif elem.is_dir() and not os.listdir(elem) and os.path.basename(elem) not in EXTENDS.keys():
            os.rmdir(elem)


def create_queue(queue: Queue, path: Path) -> Queue:
    for elem in path.iterdir():
        if elem.is_dir():
            th = Thread(target=create_queue, args=(queue, elem))
            th.start()
            th.join()
        else:
            queue.put(elem)
    return queue


def create_new_paths(queue: Queue, path_root: Path) -> list:
    new_paths = []
    for path in queue.queue:
        folder_name = ''.join([folder_name for folder_name, extend in EXTENDS.items() if path.suffix in extend])
        new_paths.append(Path.joinpath(path_root, folder_name if len(folder_name) else 'others', os.path.basename(path)))
    return new_paths


def move_files(queue: Queue, new_paths: list, locker, index: int) -> None:
    with locker:
        shutil.move(queue.queue[index], new_paths[index])


def main():
    locker = RLock()
    queue = Queue()
    path_root = Path(input('\033[1mEnter the path to the folder: \033[0m'))
    if not os.path.exists(path_root):
        print('\033[31mThere is no such folder!\033[0m')
        exit()
    start = time()
    create_basic_folders(path_root)
    remove_empty_folders(path_root)
    queue = create_queue(queue, path_root)
    new_paths = create_new_paths(queue, path_root)
    for index in range(len(new_paths)):
        th = Thread(target=move_files, args=(queue, new_paths, locker, index))
        th.start()
    finish = time()
    logger.debug(f'\033[32mThe folder was successfully sorted for:\033[0m \033[1m{finish - start} s\033[0m')
    


if __name__ == '__main__':
    main()