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
radio_buttons = []


def setup_display():
    global root, v, main_frame, radio_frame, save_button, load_button, entry_help, filename_box, radio_buttons

    root = tk.Tk()

    v = tk.IntVar()
    v.set(0)

    main_frame = tk.Frame(root)
    main_frame.grid()

    # Code to add widgets will go here...
    save_button = tk.Button(main_frame, text="Save configuration", command=save_processes)
    load_button = tk.Button(main_frame, text="Load configuration", command=load_processes)
    delete_button = tk.Button(main_frame, text="Delete configuration", command=delete_config)

    entry_help = tk.Label(main_frame, text="Configuration Name:")
    filename_box = tk.Entry(main_frame)

    save_button.grid(row=0, column=0)
    load_button.grid(row=1, column=0)
    delete_button.grid(row=2, column=0)
    entry_help.grid(row=4, column=0)
    filename_box.grid(row=5, column=0)

    saved_configs = CSV_IO.get_all_configurations(perm_processes_folder_location)

    for config in saved_configs:
        update_with_arg = partial(update_display_name, config)
        radio_button = tk.Radiobutton(main_frame,
                       text=config,
                       padx=20,
                       variable=v,
                       command=update_with_arg,
                       value=len(radio_buttons))
        radio_button.grid(row=len(radio_buttons), column=1)
        radio_buttons.append(radio_button)
    get_first_radio_button().invoke()
    reset_positions()
    root.mainloop()


def update_display_name(name):
    global filename_box
    print(name)
    filename_box.delete(0, 'end')
    filename_box.insert(0, name)


def save_processes():
    global radio_buttons
    name_to_save = filename_box.get()
    if name_to_save is not "":
        Processes.save_processes_permanently(name_to_save)
        radio_button = get_radio_button(name_to_save)
        if radio_button is None:
            update_with_arg = partial(update_display_name, name_to_save)
            radio_button = tk.Radiobutton(main_frame,
                           text=name_to_save,
                           padx=20,
                           variable=v,
                           command=update_with_arg,
                           value=len(radio_buttons))
            radio_button.grid(row=len(radio_buttons), column=1)
            radio_buttons.append(radio_button)
            get_radio_button(name_to_save).invoke()


def load_processes():
    Processes.boot_processes(filename_box.get())


def delete_config():
    global radio_buttons
    name_to_delete = filename_box.get()
    radio_button = get_radio_button(name_to_delete)
    radio_buttons.remove(radio_button)
    if radio_button is not None:
        print("deleting!")
        Processes.delete_processes(name_to_delete)
        radio_button.destroy()
        reset_positions()
        if len(radio_buttons) is not 0:
            get_first_radio_button().invoke()
        else:
            update_display_name("savedTasks")


def get_radio_button(name):
    grid_elements = main_frame.grid_slaves()
    for element in grid_elements:
        found_name = element.cget("text")
        class_type = element.winfo_class()
        print("Name: " + found_name)
        print("    \Class: " + class_type)
        if found_name == name and class_type == "Radiobutton":
            return element
    return None


def get_radio_button_position(name):
    global radio_buttons
    position = 0
    for element in radio_buttons:
        print(element)
        found_name = element.cget("text")
        class_type = element.winfo_class()
        print("Name: " + found_name)
        print("    \Class: " + class_type)
        if found_name == name and class_type == "Radiobutton":
            return position
        position += 1
    return -1


def get_first_radio_button():
    grid_elements = main_frame.grid_slaves()
    for element in grid_elements:
        found_name = element.cget("text")
        class_type = element.winfo_class()
        print("Name: " + found_name)
        print("    \Class: " + class_type)
        if class_type == "Radiobutton":
            return element


def reset_positions():
    position = 0
    for button in radio_buttons:
        button.grid(row=position, column=1)
        position += 1
