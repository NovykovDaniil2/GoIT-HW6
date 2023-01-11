def main():

    print("Hi! I'm your console assistant.")
    contact_list=[]

    while True:

        command = input("Enter the command: ").lower()

        command = command.split()
        current_command = command[0]

        #Decorator for checking functions
        def input_error(func):
            def inner(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except IndexError :
                    return "Oops! You forgot to enter the data"
                except KeyError:
                    return "Enter user name"
                except ValueError:
                    return "Enter phone"
                except TypeError:
                    return 'There is no such command or contact'
            return inner

        #Welcome function
        def hello():
            return 'How can I help you?'

        #Function for writing a number to the contact book
        @input_error
        def add_phone(command):
            contact_list.append({command[1] : command[2]})
            return 'The contact was recorded successfully!'

        #Function for making changes to the number in the contact book
        @input_error
        def change_phone(command):
            for contact in contact_list:
                if command[1] in contact:
                    contact[command[1]] = command[2]
                    return 'The contact was changed successfully!'
                else:
                    raise TypeError()

        #Function for determining the phone number by the contact name
        @input_error
        def check_phone(command):
            for contact in contact_list:
                if command[1] in contact:
                    return f"{command[1]} : {contact.get(command[1])}"
            if command[1] not in contact_list:
                raise TypeError()

        #Function for displaying all existing contacts
        @input_error
        def show_phones(command):
            if 'show' and 'all' in command:
                for contact in contact_list:
                    for key, value in contact.items():
                        print("{0} : {1}".format(key,value))
                if len(contact_list) == 0:
                    return 'The contact list is empty'
                else:
                    return 'All contacts have been successfully printed!'
            raise TypeError()

        #The farewell function
        @input_error
        def good_bye(command):
            if 'good' and 'bye' in command or 'close' in command or 'exit' in command:
                print("Good bye!")
                exit()
            raise TypeError()


        COMMANDS={
            'hello' : hello,
            'add' : add_phone,
            'change' : change_phone,
            'phone' : check_phone,
            'show' : show_phones,
            'good' : good_bye,
            'close' : good_bye,
            'exit' : good_bye
        }

        #A function for recognizing and running the required commands
        def get_handler(current_command):
            if current_command in COMMANDS:
                handler = COMMANDS[current_command]
                try:
                    return handler(command)
                except TypeError:
                    return handler()
            else:
                return 'There is no such command'

        print(get_handler(current_command))
        

if __name__ == '__main__':
    main()



