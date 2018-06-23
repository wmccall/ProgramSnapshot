import Processes
from tkinter import *


def main():
    choice = ""

    root = Tk()

    frame = Frame(root)
    frame.pack()

    # Code to add widgets will go here...
    save_button = Button(frame, text="Save programs", command=Processes.save_processes_permanently)
    load_button = Button(frame, text="Load programs", command=Processes.boot_processes)
    save_button.pack(side=LEFT)
    load_button.pack(side=RIGHT)
    root.mainloop()



    while choice is not "3":
        while choice is not "1" and choice is not "2" and choice is not "3":
            choice = input("[1]: Load programs\n[2]: Save programs\n[3]: Quit\n")
            print("Choice: " + choice)

        if choice is "1":
            Processes.boot_processes()
            choice = ""
        if choice is "2":
            Processes.save_processes_permanently()
            choice = ""

    print("Quitting")

if __name__ == "__main__":
    main()

