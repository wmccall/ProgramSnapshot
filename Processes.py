import subprocess
import re

import os

import CSV_IO


temp_processes_folder_location = ".\\tempconfig"
temp_process_file_name = "tempTasks.csv"

perm_processes_folder_location = ".\\configs"
perm_process_file_name = "savedTasks.csv"


def get_raw_processes():
    cmd = 'WMIC PROCESS get Caption,Commandline'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return proc.stdout


def clean_names_and_remove_services(processes):
    refined_processes = []
    for process in processes:
        name_and_location_sub_list = re.compile(r'\s\s+').split(process.decode('utf8'))

        subelements = 0
        name_and_location_sub_list_cleaned = []
        element_is_legit = True
        for element in name_and_location_sub_list:
            subelements += 1
            if subelements == 1:
                element.replace("b'", "")
            elif subelements == 2:
                while element.find('\\\\') != -1:
                    element = element.replace('\\\\', '\\')
                element = delete_parameters(element)
                while element.find('"') != -1:
                    element = element.replace('"', '')
                if len(element) < 1 or element.lower().find("c:\windows\system32") > 0:
                    element_is_legit = False

            name_and_location_sub_list_cleaned.append(str(element))

        if subelements == 3 and element_is_legit and not is_duplicate_process(refined_processes, name_and_location_sub_list_cleaned[0: 2]):
            refined_processes.append(name_and_location_sub_list_cleaned[0: 2])

    return sorted(refined_processes, key=lambda x: (x[0].lower(), x[1].lower()))


def delete_parameters(element):
    end_of_program_location = element.find('.exe')
    if end_of_program_location == -1:
        return ""
    return element[0:end_of_program_location+4]


def is_duplicate_process(found_processes, new_process):
    # print("NewProcess:" + new_process[0])
    for process in sorted(found_processes, key=lambda x: (x[0].lower(), x[1].lower())):
        # print(process[0])
        if process[0] == new_process[0]:
            # print("   \\ is duplicate")
            return True
    # print("   \\ is unique")
    return False


def refine_raw_processes(processes):
    cleaned_processes = clean_names_and_remove_services(processes)
    return cleaned_processes


def get_processes():
    raw_processes = get_raw_processes()
    processes = refine_raw_processes(raw_processes)
    return processes


def save_processes(filename):
    CSV_IO.write_processes(get_processes(), filename)


def save_processes_permanently():
    os.makedirs(os.path.dirname(perm_processes_folder_location + "\\" + perm_process_file_name), exist_ok=True)
    save_processes(perm_processes_folder_location + "\\" + perm_process_file_name)


def save_processes_temporarily():
    os.makedirs(os.path.dirname(temp_processes_folder_location + "\\" + temp_process_file_name), exist_ok=True)
    save_processes(temp_processes_folder_location + "\\" + temp_process_file_name)


def boot_processes():
    save_processes_temporarily()
    temp_processes = CSV_IO.read_processes(temp_processes_folder_location + "\\" + temp_process_file_name)
    saved_processes = CSV_IO.read_processes(perm_processes_folder_location + "\\" + perm_process_file_name)

    for process in sorted(saved_processes, key=lambda x: (x[0].lower(), x[1].lower())):
        if not is_duplicate_process(temp_processes, process):
            print("running " + process[1])
            run_process(process)


def run_process(process):
    subprocess.Popen(process[1], shell=True,
                     stdin=None, stdout=None, stderr=None, close_fds=True)
