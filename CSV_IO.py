import csv
import os

from Program import perm_processes_folder_location

config_count = 0


def write_processes_to_file(processes, file_location):
    global config_count

    if not os.path.isfile(file_location):
        config_count += 1
    with open(file_location, 'w', newline='') as taskfile:
        writer = csv.writer(taskfile)
        writer.writerows(processes)


def read_processes_in_file(file_location):
    processes = []
    with open(file_location, 'r') as taskfile:
        reader = csv.reader(taskfile)
        for row in reader:
            processes.append(row)

    return processes


def delete_configuration(file_location):
    global config_count

    config_count -= 1

    os.remove(file_location)


def get_all_configurations(folder_location):
    global config_count

    config_count = 0
    configurations = []
    try:
        for itemName in os.listdir(folder_location):
            path_to_item = os.path.join(folder_location, itemName)
            if os.path.isfile(path_to_item) and itemName[-4:] == ".csv":
                configurations.append(itemName[:-4])
                config_count += 1
    except FileNotFoundError:
        print("Creating config folder")
        os.mkdir(perm_processes_folder_location)
    return configurations


def get_config_count():
    global config_count

    return config_count
