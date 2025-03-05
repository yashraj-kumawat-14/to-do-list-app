from tkinter import Tk, Frame, Entry, StringVar, Button, Label, Toplevel
from tkcalendar import DateEntry
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
from time import sleep
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("worked path : ",os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.Tasks import Tasks

# Get the absolute path to the current script
current_script_path = os.path.abspath(__file__)
print("current_script_path: ", current_script_path)

# Extract the directory path
directory_path = os.path.dirname(current_script_path)
print("directory_path : ",directory_path)

# Navigate up to the 'result_management' directory (assuming it's the parent directory)
parent_directory = os.path.dirname(directory_path)
print("parent_directory : ", parent_directory)


class AddTask:
    def __init__(self, root, parentCallback=None):
        self.parentCallback = parentCallback
        self.root = root
        self.addTaskModal = Toplevel(root) # create a seprate window from main window using toplevel widget
        # self.addTaskModal.geometry("300x300")
        self.addTaskModal.resizable(False, False)

        self.addTaskModal.title("Add Task")
        self.addTaskModal.transient(root) # transient(self.root) makes the toplevel window keeping attached with main window root, and doesn't get seprated
        
        self.addTaskModal.update_idletasks() # using it to render the toplevel window before making it a model or can say using the grab-set method
        self.addTaskModal.grab_set() # prevent interaction with main window root until it is closed, but before calling this toplevel should be rendered before
        
        self.messageLabel = Label(self.addTaskModal, text="", bg="black")
        self.messageLabel.pack(fill="x")
        
        self.mainFrame = Frame(self.addTaskModal)
        self.mainFrame.pack(fill="both", expand=True)
        
        Label(self.mainFrame, text="Name : ").grid(row=0, column=0, sticky="e")
        Label(self.mainFrame, text="Date/Time : ").grid(row=1, column=0, sticky="e")
        Label(self.mainFrame, text="Priority : ").grid(row=2, column=0, sticky="e")
        Label(self.mainFrame, text="Status : ").grid(row=3, column=0, sticky="e")
        
        self.taskVar = StringVar(value="")
        self.taskEntry = Entry(self.mainFrame, textvariable=self.taskVar)
        self.taskEntry.grid(row=0, column=1, sticky="w")
        
        self.dateEntry = DateEntry(self.mainFrame, state="readonly")
        self.dateEntry.grid(row=1, column=1, sticky="we")
        
        self.priorityVar = StringVar(value="★")
        self.priorityEnty = Entry(self.mainFrame, textvariable=self.priorityVar, state="readonly")
        self.priorityEnty.grid(row=2, column=1, sticky="wens")
        
        self.upDownBtnFrame = Frame(self.mainFrame)
        self.upDownBtnFrame.grid(row=2, column=2)
        
        # Up and Down Arrow Buttons
        self.btn_up = Button(self.upDownBtnFrame, text="▲", font="COPPER 6", width=2, height=1, command=self.increase_priority)
        self.btn_up.grid(row=0, column=0)
        
        self.btn_down = Button(self.upDownBtnFrame, text="▼", font="COPPER 6", width=2, height=1, command=self.decrease_priority)
        self.btn_down.grid(row=1, column=0)        
        
        self.statusVar = StringVar(value="")
        
        self.statusDropDown = Combobox(self.mainFrame, state="readonly", textvariable=self.statusVar, values=["Todo", "Done"])
        self.statusDropDown.grid(row=3, column=1, sticky="w")
        
        self.statusDropDown.set("Todo")
        
        self.saveBtn = Button(self.mainFrame, text="Save", bg="orange", fg="white", command=self.save)
        self.saveBtn.grid(row=4, column=0, columnspan=3, pady=(10, 10), sticky="we", padx=(5, 5))

    def increase_priority(self):
        if len(self.priorityVar.get())<3:
            self.priorityVar.set(self.priorityVar.get()+"★")
        else:
            showinfo("Max Prioriy", "Three ★ are the maximum priority.")
            
    def decrease_priority(self):
        if len(self.priorityVar.get())<2:
            showinfo("Least Prioriy", "Single ★ is the least priority.")
        else:
            self.priorityVar.set(self.priorityVar.get()[:-1])
            
    def save(self):
        name = self.taskVar.get()
        date = self.dateEntry.get()
        priority = len(self.priorityVar.get())
        status = self.statusVar.get()
        
        print(f"name {name}, date {date}, priority {priority}, status {status}")
        
        if(not status or not name or not date):
            self.messageLabel.config(text="Please fill all the details.", fg="red")
            return None
        try:
            model = Tasks()
            model.add_task(name=name, date=date, priority=priority, status=status)
            self.messageLabel.config(text="Success Task is added.", fg="green")
            self.addTaskModal.update()
            sleep(2)
            if(self.parentCallback):
                self.parentCallback(cmd="refresh")
            self.addTaskModal.destroy()
        except Exception as e:
            self.messageLabel.config(text="Error Task is didn't add.", fg="red")
            print("Error: ", e)
    
if __name__ == "__main__":
    root = Tk()
    AddTask(root)
    root.mainloop()

