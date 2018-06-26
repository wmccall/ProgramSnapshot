import Display

temp_processes_folder_location = ".\\tempconfig"
temp_process_file_name = "tempTasks.csv"

temp_process_file_location = temp_processes_folder_location + "\\" + temp_process_file_name


perm_processes_folder_location = ".\\configs"
default_perm_process_file_name = "savedTasks.csv"

extension = ".csv"


def main():
    Display.setup_display()

if __name__ == "__main__":
    main()
