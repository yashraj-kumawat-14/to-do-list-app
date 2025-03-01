from tkinter import Tk, PhotoImage

class App:
    def __init__(self, title="To-Do List Application", width=700, height=500):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        icon = PhotoImage(file="./assets/app_icon.png")
        self.root.iconphoto(False, icon)
        self.root.mainloop()
        

if __name__ == "__main__":
    App()