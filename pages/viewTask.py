from tkinter import Tk, Frame, Entry, StringVar, Button, Label, Toplevel
from tkcalendar import DateEntry
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
import os
from time import sleep
from sys import path

# Get the absolute path to the current script
current_script_path = os.path.abspath(__file__)

# Extract the directory path
directory_path = os.path.dirname(current_script_path)
print(directory_path)

# Navigate up to the 'result_management' directory (assuming it's the parent directory)
parent_directory = os.path.dirname(directory_path)
print(parent_directory)

path.append(f"{parent_directory}/model")

from Tasks import Tasks

class ViewTask:
    def __init__(self, root, taskId=None, parentCallback=None):
        self.parentCallback = parentCallback
        self.taskId=taskId
        
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
        
        self.deleteBtn = Button(self.mainFrame, text="Delete", bg="red", fg="white", command=self.delete)
        self.deleteBtn.grid(row=4, column=2, pady=(10, 10), sticky="we", padx=(5, 5))
        
        self.load_data()
        

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
            self.messageLabel.config(text="Please fill all the details", fg="red")
            return None
        if not self.taskId:
            self.messageLabel.config(text="Task id is missing.", fg="orange")
            return None
        try:
            model = Tasks()
            model.update_task(id=self.taskId, name=name, date=date, priority=priority, status=status)
            self.messageLabel.config(text="Success Task is updated.", fg="green")
            self.addTaskModal.update()
            sleep(2)
            self.addTaskModal.destroy()
        except Exception as e:
            self.messageLabel.config(text="Error Task is didn't updated.", fg="red")
            print("Error: ", e)
    
    def load_data(self):
        if(self.taskId):
            model = Tasks()
            data = model.get_task_by_id(id=self.taskId)
            self.taskVar.set(data[1])
            self.dateEntry.set_date(data[4])
            self.statusVar.set(data[3])
            self.priorityVar.set("★"*int(data[2]))
            
    
    def delete(self):
        if not self.taskId:
            self.messageLabel.config(text="Task id is missing.", fg="orange")
            return None
        
        try:
            model = Tasks()
            model.delete_task(id=self.taskId)
            self.messageLabel.config(text="Success Task is deleted.", fg="green")
            self.addTaskModal.update()
            sleep(2)
            if(self.parentCallback):
                print("called refresh")
                self.parentCallback(cmd="refresh")
            self.addTaskModal.destroy()
        except Exception as e:
            print(f"error occured {e}")
    
if __name__ == "__main__":
    root = Tk()
    ViewTask(root, taskId=8)
    root.mainloop()

