import csv


def write_processes(processes, filename):
    with open(filename, 'w', newline='') as taskfile:
        writer = csv.writer(taskfile)
        writer.writerows(processes)


def read_processes(filename):
    processes = []
    with open(filename, 'r') as taskfile:
        reader = csv.reader(taskfile)
        for row in reader:
            processes.append(row)

    return processes

