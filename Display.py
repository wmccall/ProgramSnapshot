import Processes
import tkinter as tk
from functools import partial
import CSV_IO
from Program import perm_processes_folder_location
from Program import default_perm_process_file_name

root = None
v = None
main_frame = None
radio_frame = None
save_button = None
load_button = None
entry_help = None
filename_box = None


def setup_display():
    global root, v, main_frame, radio_frame, save_button, load_button, entry_help, filename_box

    root = tk.Tk()

    v = tk.IntVar()
    v.set(0)

    main_frame = tk.Frame(root)
    main_frame.grid()

    # Code to add widgets will go here...
    save_button = tk.Button(main_frame, text="Save programs", command=Processes.save_processes_permanently)
    load_button = tk.Button(main_frame, text="Load programs", command=Processes.boot_processes)

    entry_help = tk.Label(main_frame, text="Configuration Name:")
    filename_box = tk.Entry(main_frame)

    save_button.grid(row=0, column=0)
    load_button.grid(row=1, column=0)
    entry_help.grid(row=4, column=0)
    filename_box.grid(row=5, column=0)

    saved_configs = CSV_IO.get_all_configurations(perm_processes_folder_location)

    local_count = 0
    for config in saved_configs:
        update_with_arg = partial(update_display_name, config)
        tk.Radiobutton(main_frame,
                       text=config,
                       padx=20,
                       variable=v,
                       command=update_with_arg,
                       value=local_count).grid(row=local_count, column=1)
        local_count += 1

    root.mainloop()


def update_display_name(name):
    global filename_box
    print(name)
    filename_box.delete(0, 'end')
    filename_box.insert(0, name)
