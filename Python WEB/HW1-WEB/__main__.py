from Bot import *

if __name__ == "__main__":

    print('Hello. I am your contact-assistant. What should I do with your contacts?')

    bot = Bot()
    bot.book.load("auto_save")

    while True:

        action = input('Type help for list of commands or enter your command\n').strip().lower()

        if action == 'exit':
            exit()
            
        try:
            performer(get_handler(action), bot)
        except:
            print('There is no such command!')