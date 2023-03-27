import os
import shutil
from prettytable import PrettyTable

#Dict for normalize()
transliterate_dict = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'Shch','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'Ya','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '.':'.', 'x':'x', 'X':'X', 'j':'j', 'J':'J', 'w':'w', 'W':'W'}


# List of numbers for the normalize() function
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

# Folders to skip
ignore_folders = ["images", "video", "documents", "audio", "archives", "other"]

EXTENDS = {
    ("png", "jpeg", "jpg", "svg"): "\\images\\",
    (".avi", ".mp4", ".mov", ".mkv"): "\\video\\",
    (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"): "\\documents\\",
    (".mp3", ".ogg", ".wav", ".amr"): "\\audio\\",
    (".zip", ".tar", ".gz"): "\\archives\\",
}

#File sorted counter
counter = {category: 0 for category in ignore_folders}


# Function to normalize the file name
def normalize(file_name: str) -> str:
    for key in transliterate_dict:
        file_name = file_name.replace(key, transliterate_dict.get(key))
    for i in file_name:
        if (
            i not in transliterate_dict.values()
            and i not in transliterate_dict.keys()
            and i not in numbers
        ):
            file_name = file_name.replace(i, "_")
    return file_name


def create_folders(path):
    for ignore_folder in ignore_folders:
        if ignore_folder not in os.listdir(path):
            os.mkdir(path + "\\" + ignore_folder)
    return "Folder to sort has been created"


# Recursive folder sort function
def sorting_function(path):
    for elem in os.listdir(path):
        # The basic part
        if len(elem.split(".")) > 1:
            for extend, category in EXTENDS.items():
                if os.path.splitext(elem)[-1] in extend:
                    current_file = path + "\\" + elem
                    new_path = path + category + normalize(elem)
                    counter[category[1:-1]] += 1
                    #os.rename(current_file, new_path)
                    shutil.move(current_file, new_path)

            if os.path.splitext(elem)[-1] not in [extend for extends_tup in EXTENDS.keys() for extend in extends_tup]:
                current_file = path + "\\" + elem
                new_path = path + "\\other\\" + normalize(elem)
                counter["other"] += 1
                shutil.move(current_file, new_path)

        # The recursive part
        if (
            os.path.isdir(path + "\\" + elem)
            and len(os.listdir(path + "\\" + elem)) == 0
            and elem not in ignore_folders
        ):
            os.rmdir(path + "\\" + elem)
        elif os.path.isdir(path + "\\" + elem) and elem not in ignore_folders:
            sorting_function(path + "\\" + elem)

    return "The folder has been sorted!"


def start_sorting():
    path = input("\033[1mEnter the path to the folder to sort: ")
    try:
        create_folders(path)
        print(sorting_function(path))
    except FileNotFoundError:
        return "\033[31mThere is no such file\033[0m"
    table = PrettyTable()
    table.field_names = ["Filetype", "Count"]
    for category, count in counter.items():
        table.add_row([category, count])
    return table

