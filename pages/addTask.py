from tkinter import Tk, PhotoImage, Frame, Entry, StringVar, Button, Label, Listbox, Toplevel
from tkcalendar import DateEntry
from tkinter.ttk import Combobox

class AddTask:
    def __init__(self, root):
        self.root = root
        self.addTaskModal = Toplevel(root) # create a seprate window from main window using toplevel widget
        self.addTaskModal.geometry("300x300")

        self.addTaskModal.title("Add Task")
        self.addTaskModal.transient(root) # transient(self.root) makes the toplevel window keeping attached with main window root, and doesn't get seprated
        
        self.addTaskModal.update_idletasks() # using it to render the toplevel window before making it a model or can say using the grab-set method
        self.addTaskModal.grab_set() # prevent interaction with main window root until it is closed, but before calling this toplevel should be rendered before
        
        self.mainFrame = Frame(self.addTaskModal)
        self.mainFrame.pack(fill="both", expand=True)
        
        Label(self.mainFrame, text="Name : ").grid(row=0, column=0, sticky="e")
        Label(self.mainFrame, text="Date/Time : ").grid(row=1, column=0, sticky="e")
        Label(self.mainFrame, text="Priority : ").grid(row=2, column=0, sticky="e")
        Label(self.mainFrame, text="Status : ").grid(row=3, column=0, sticky="e")
        
        self.taskEntryVar = StringVar(value="")
        self.taskEntry = Entry(self.mainFrame, textvariable=self.taskEntryVar)
        self.taskEntry.grid(row=0, column=1, sticky="w")
        
        self.dateVar = StringVar(value="")
        self.dateEntry = DateEntry(self.mainFrame, state="readonly")
        self.dateEntry.grid(row=1, column=1, sticky="we")
        
        self.priorityVar = StringVar(value="")
        self.priorityEnty = Entry(self.mainFrame, textvariable=self.priorityVar, state="readonly")
        self.priorityEnty.grid(row=2, column=1, sticky="wens")
        
        self.upDownBtnFrame = Frame(self.mainFrame)
        self.upDownBtnFrame.grid(row=2, column=2)
        
        # Up and Down Arrow Buttons
        self.btn_up = Button(self.upDownBtnFrame, text="▲", font="COPPER 6", width=2, height=1)
        self.btn_up.grid(row=0, column=0)
        
        self.btn_down = Button(self.upDownBtnFrame, text="▼", font="COPPER 6", width=2, height=1)
        self.btn_down.grid(row=1, column=0)        
        
        self.statusVar = StringVar(value="")
        
        self.statusDropDown = Combobox(self.mainFrame, state="readonly", textvariable=self.statusVar, values=["Todo", "Pending", "Done"])
        self.statusDropDown.grid(row=3, column=1, sticky="w")
        
        self.statusDropDown.set("select...")
        
        self.saveBtn = Button(self.mainFrame, text="Save", bg="orange", fg="white")
        self.saveBtn.grid(row=4, column=0, columnspan=3, pady=(10, 10), sticky="we", padx=(5, 5))

        
if __name__ == "__main__":
    root = Tk()
    AddTask(root)
    root.mainloop()

