import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.configure(bg='gray')

        self.display = tk.Entry(master, width=20, font=('Arial', 20))
        self.display.grid(row=0, column=0, columnspan=4, pady=5)

        buttons = {'7' : (1,0), '8' : (1,1), '9' : (1,2), '/' : (1,3),
                   '4' : (2,0), '5' : (2,1), '6' : (2,2), '*' : (2,3),
                   '1' : (3,0), '2' : (3,1), '3' : (3,2), '-' : (3,3),
                   '0' : (4,0), '.' : (4,1), 'C' : (4,2), '+' : (4,3),}
        
        for button, coordinates in buttons.items():
            self.create_button(button, *coordinates)
        self.create_button('=', 5, 0, columnspan=4)

    def create_button(self, text, row, column, columnspan=1):
        button = tk.Button(self.master, text=text, font=('Arial', 16), width=5, height=2, bg='#131313', fg='white', command=lambda: self.button_click(text))
        button.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5)

    def button_click(self, text):
        if text == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, 'Error')
        elif text == 'C':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, text)


def start_calc():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
    return '\033[32mThank you for using the calculator'
