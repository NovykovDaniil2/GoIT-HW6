import os
import shutil
import sys


#Folders to skip
ignore_folders = ['archives', 'video', 'audio', 'documents', 'images']


#Dict for normalize()
transliterate_dict = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '.':'.', 'x':'x', 'X':'X', 'j':'j', 'J':'J', 'w':'w', 'W':'W'}


#List of numbers for the normalize() function
numbers = ['1','2','3','4','5','6','7','8','9']


#Function to normalize the file name
def normalize(file_name: str) -> str:
    for key in transliterate_dict:
        file_name = file_name.replace(key, transliterate_dict.get(key))
    for i in file_name:
        if i not in transliterate_dict.values() and i not in transliterate_dict.keys() and i not in numbers:
            file_name = file_name.replace(i, '_')
    return file_name


#Recursive folder sort function
def sorting_function(path):
    for ignore_folder in ignore_folders:
        if ignore_folder not in os.listdir(path):
            os.mkdir(path + '\\' + ignore_folder)
    for elem in os.listdir(path):
        #The basic part
        if len(elem.split('.'))>1:

            if elem.lower().endswith(('.jpeg', '.png', '.jpg', '.svg')):
                current_file = path + '\\' + elem
                new_path = path + '\\images\\' + normalize(elem)
                shutil.move(current_file, new_path)

            elif elem.lower().endswith(('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')):
                current_file = path + '\\' + elem
                new_path = path + '\\documents\\' + normalize(elem)
                shutil.move(current_file, new_path)

            elif elem.lower().endswith(('.avi', '.mp4', '.mov', '.mkv')):
                current_file = path + '\\' + elem
                new_path = path + '\\video\\' + normalize(elem)
                shutil.move(current_file, new_path)

            elif elem.lower().endswith(('.mp3', '.ogg', '.wav', '.amr')):
                current_file = path + '\\' + elem
                new_path = path + '\\audio\\' + normalize(elem)
                shutil.move(current_file, new_path)

            elif elem.lower().endswith(('.zip', '.gz', '.tar')):
                os.mkdir(path + '\\archives\\' + elem.split('.')[0])
                os.rename( path + '\\archives\\' + elem.split('.')[0], path + '\\archives\\' + normalize(elem.split('.')[0]))
                shutil.unpack_archive(path + '\\' + elem, path + '\\archives\\' + elem.split('.')[0], elem.split('.')[1])
                os.remove(path + '\\' + elem)
                
                
        #The recursive part
        if os.path.isdir(path + '\\' + elem) and len(os.listdir(path + '\\' + elem))==0 and elem not in ignore_folders :
            os.rmdir(path + '\\' + elem)
        elif os.path.isdir(path+'\\'+elem) and elem not in ignore_folders:
            sorting_function(path+'\\'+ elem)

def main():
    sorting_function(sys.argv[1])
if __name__ == '__main__':
    main()


    
