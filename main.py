from tkinter import Tk, PhotoImage, Frame, Entry, StringVar, Button, Label, Listbox
from tkinter.messagebox import showinfo
from pages.addTask import AddTask
from tkinter import ttk
import os
from sys import path

current_script_path = os.path.abspath(__file__)
directory_path = os.path.dirname(current_script_path)
parent_dir_path = os.path.dirname(directory_path)

path.append(parent_dir_path)
from Tasks import Tasks

class App:
    def __init__(self, title="To-Do List Application", width=800, height=470):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.icon = PhotoImage(file="./assets/app_icon.png")
        self.root.iconphoto(False, self.icon)
        
        self.root.resizable(False, False)
        
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(fill="both", expand=True)
        
        self.appHeading = Label(self.mainFrame, text="Todoist", bg="black", fg="white", font=("COPPER", 15, "bold"))
        self.appHeading.pack(fill="x")
        
        self.searchFrame = Frame(self.mainFrame, bg="grey")
        self.searchFrame.pack(side="top", fill="x")
        
        self.searchFrame.rowconfigure(0, weight=1)
        self.searchFrame.columnconfigure(0, weight=1)
        
        self.searchPlaceholder = "\U0001F50D  Search"
        self.searchIcon = "\U0001F50D"
        
        self.searchQuery = StringVar()
        self.searchQuery.set(self.searchPlaceholder)
        
        self.searchEntry = Entry(self.searchFrame, textvariable=self.searchQuery)
        self.searchEntry.grid(row=0, column=0, sticky="ew")
        
        self.searchBtn = Button(self.searchFrame, text=self.searchIcon)
        self.searchBtn.grid(row=0, column=1)
        
        self.searchEntry.bind("<FocusIn>", lambda event: self.clearPlaceholder(event, self.searchQuery))
        self.searchEntry.bind("<FocusOut>", lambda event: self.putPlaceholder(event, self.searchPlaceholder, self.searchQuery))
        
        self.tasksFrame = Frame(self.mainFrame, bg="orange")
        self.tasksFrame.pack(fill="both", expand=True)
        
        self.tasksFrame.rowconfigure(0, weight=1)
        self.tasksFrame.columnconfigure(0, weight=1)
        
        self.tasksTable = ttk.Treeview(self.tasksFrame, columns=("task", "status", "date", "priority"))
        self.tasksTable.grid(row=0, column=0, sticky="nsew")
        
        self.tasksTable.column("#0", width=40, stretch=False, anchor="center")
        self.tasksTable.column("task", width=100, minwidth=50, anchor="center")
        self.tasksTable.column("status", width=100, minwidth=50, anchor="center")
        self.tasksTable.column("date", width=100, minwidth=50, anchor="center")
        self.tasksTable.column("priority", width=100, minwidth=50, anchor="center")
        
        self.tasksTable.heading("#0", text="id", anchor="center")
        self.tasksTable.heading("task", text="Task", anchor="center")
        self.tasksTable.heading("status", text="Status", anchor="center")
        self.tasksTable.heading("date", text="Date", anchor="center")
        self.tasksTable.heading("priority", text="Priority", anchor="center")
        
        self.actionFrame = Frame(self.mainFrame)
        self.actionFrame.pack(fill="x", side="bottom")
        
        self.actionFrame.rowconfigure(0, weight=1)
        self.actionFrame.columnconfigure(0, weight=1)
        self.actionFrame.columnconfigure(1, weight=1)
        
        self.addTaskBtn = Button(self.actionFrame, text="+  Add", font=("COPPER", 11, 'bold'))
        self.addTaskBtn.grid(row=0, column=0, sticky="we")
        
        self.viewTaskBtn = Button(self.actionFrame, text="\U0001F441 View Selected")
        self.viewTaskBtn.grid(row=0, column=1, sticky="we")
        
        self.addTaskBtn.bind("<Button-1>", self.addTask)

        self.insertData()
        
        self.root.mainloop()
        
    def clearPlaceholder(self, event, searchQuery):
        searchQuery.set("")
            
        
    def putPlaceholder(self, event, placeholder, searchQuery):
        searchQuery.set(placeholder)
        
    def addTask(self, event):
        AddTask(self.root)
        
    def insertData(self):
        model = Tasks()
        data = model.get_tasks()
        for row in data:
            print(row)
            self.tasksTable.insert("", "end", text=row[0], values=(row[1], row[3], row[4], "★"*int(row[2])))

if __name__ == "__main__":
    App()