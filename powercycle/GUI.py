import tkinter as tk
from tkinter import *
from db_interaction import *
import os


form_self = None

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared = {"email": tk.StringVar()}
        container = tk.Frame(self)
        container.pack()
        self.geometry("1200x800")
        self.title("Bicycle Application")

        menu = Menu(self)
        self.config(menu=menu)

        # create home menu
        menu.add_cascade(label="Home", command=lambda: self.show("Home"))

        # create file menu
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        self.frames = {}
        for F in (Home, Calibrate, EnterEmail, Form, Run):
            page = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("Home")

    # define show function
    def show(self, page):
        frame = self.frames[page]
        frame.tkraise()

# create home page
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Welcome to Performance Cycling System !", font=("Courier", 32), fg="black",)
        title.grid(row=0, column=1, padx=30, pady=30)

        calibrate_button = tk.Button(self, text="Calibrate", height=2, width=10,
                                     bg="deep sky blue", command=lambda: controller.show("Calibrate"))
        calibrate_button.grid(row=1, column=1, padx=15, pady=15)
        run_button = tk.Button(self, text="Run", height=4, width=20,
                               bg="sea green", command=lambda: controller.show("EnterEmail"))
        run_button.grid(row=2, column=1, padx=2, pady=2)

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

# create calibration page
class Calibrate(tk.Frame):
    def __init__(self, parent, controller):
        def run_script():
            os.system('python Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Calibration", font=("Courier", 44), fg="black")
        title.grid(row=1, column=1)
        calibrate_button = tk.Button(self, text="Run Calibration", height=4, width=24, bg="sea green", command=run_script)
        calibrate_button.grid(row=2, column=1, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create lookup by email page
class EnterEmail(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        title = tk.Label(self, text="Enter Email:", font=("Courier", 28), fg="black")
        title.grid(row=19, column=40)
        e = tk.Entry(self, textvariable=self.controller.shared["email"])
        e.grid(row=20, column=40, sticky="nsew")
        def submit():
            global form_self
            email(form_self)
            search = email_search(e.get())
            if search == None:
                controller.show("Form")
            else:
                controller.show("Run")
        find_button = tk.Button(self, text="Find", height=2, width=8, bg="deep sky blue", command=submit)
        find_button.grid(row=25, column=40, padx=2, pady=2)
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


def email(self):
    email = self.controller.shared["email"].get()
    self.title = tk.Label(self, text="Email: " + email, font=("Courier", 28), fg="black")
    self.title.grid(row=1, columnspan=4)

class Form(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global form_self
        form_self = self
        s = tk.StringVar()
        Label(self, text="First Name", font=("Courier", 14)).grid(row=2, column=1, pady=2)
        Label(self, text="Last Name", font=("Courier", 14)).grid(row=3, column=1, pady=2)
        Label(self, text="Age", font=("Courier", 14)).grid(row=4, column=1, pady=2)
        Label(self, text="Height", font=("Courier", 14)).grid(row=5, column=1, pady=2)
        Label(self, text="Weight", font=("Courier", 14)).grid(row=6, column=1, pady=2)
        Label(self, text="Sex", font=("Courier", 14)).grid(row=7, column=1, pady=2)
        Label(self, text="Category", font=("Courier", 14)).grid(row=9, column=1, pady=2)
        entry1 = Entry(self)
        entry2 = Entry(self)
        entry3 = Entry(self)
        entry4 = Entry(self)
        entry5 = Entry(self)
        entry6 = tk.Radiobutton(self, text="Male", variable=s, value="Male")
        entry7 = tk.Radiobutton(self, text="Female", variable=s, value="Female")
        entry8 = Entry(self)
        entry1.grid(row=2, column=2, pady=2)
        entry2.grid(row=3, column=2, pady=2)
        entry3.grid(row=4, column=2, pady=2)
        entry4.grid(row=5, column=2, pady=2)
        entry5.grid(row=6, column=2, pady=2)
        entry6.grid(row=7, column=2, pady=2)
        entry7.grid(row=8, column=2, pady=2)
        entry8.grid(row=9, column=2, pady=2)

        def submit(email, fname, lname, age, height, weight, gender, category):
            user_insert(email, fname, lname, age, height, weight, gender, category)
            controller.show("Run")

        submit_button = tk.Button(self, text="Submit", height=2, width=12, command=lambda: submit(self.controller.shared["email"].get(), entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), s.get(), entry8.get()))
        submit_button.grid(row=10, column=2)

        self.grid_rowconfigure(0, weight=1, minsize=150)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(11, weight=1)
        self.grid_columnconfigure(3, weight=1)

class Run(tk.Frame):
    def __init__(self, parent, controller):
        def run_script():
            os.system('python Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Run Bicycle", font=("Courier", 44), fg="black")
        title.grid(row=1, column=1)
        run_button = tk.Button(self, text="Run", height=4, width=24, bg="sea green", command=run_script)
        run_button.grid(row=2, column=1, padx=2, pady=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()