import os


def task1(path, only_directories=False, only_files=False):
    if (only_directories and only_files) or os.path.isfile(path):
        return []

    result = []
    for name in os.listdir(path):
        if not only_directories and os.path.isfile(os.path.join(path, name)):
            result.append(name)
        elif not only_files and not os.path.isfile(os.path.join(path, name)):
            result.append(name)

    return result


def task2(path):
    payload = {
        "accessible": False,
        "readable": False,
        "writable": False,
        "executable": False,
    }

    payload["accessible"] = os.access(path, os.F_OK)
    if not payload["accessible"]:
        return payload

    payload["readable"] = os.access(path, os.R_OK)
    payload["writable"] = os.access(path, os.W_OK)
    payload["executable"] = os.access(path, os.X_OK)

    return payload


def task3(path):
    result = {
        "accessible": False,
        "filename": "",
        "dirname": "",
    }

    result["accessible"] = os.access(path, os.F_OK)
    if not result["accessible"]:
        return result

    if not os.path.isfile(path):
        result["dirname"] = os.path.abspath(path)
        return result

    result["dirname"] = os.path.dirname(os.path.abspath(path))
    result["filename"] = os.path.basename(os.path.abspath(path))

    return result


def task4(path):
    f = open(path, "r")
    lines = 0
    for _ in f:
        lines += 1

    return lines


def task5(path, arr):
    f = open(path, "w")
    for i, el in enumerate(arr):
        f.write(str(el))
        if i + 1 != len(arr):
            f.write("\n")


def task6(path):
    for i in range(26):
        open(os.path.join(path, f"{chr(ord('A') + i)}.txt"), "w+")


def task7(path_from, path_to):
    stat_from = task3(path_from)
    stat_to = task3(path_to)

    if not stat_from["filename"]:
        raise "Specified source path is not a file"
    filename = stat_from["filename"]

    if not stat_to["dirname"]:
        raise "Specified destination path does not exists"

    file_from = open(path_from, "r")
    file_new = open(os.path.join(path_to, filename), "w+")

    for line in file_from:
        file_new.write(line)


def task8(path):
    stat = task3(path)
    if not stat["dirname"]:
        return

    if stat["filename"]:
        os.remove(path)
    else:
        os.rmdir(path)


path_lab6 = "Lab 06\\"
path_poligon = "Lab 06\\poligon"
path_this = "Lab 06\\dir_and_files.py"
path_not_existing = "Not Existing"
path_sample4 = "Lab 06\\poligon\\sample4.txt"
path_sample5 = "Lab 06\\poligon\\sample5.txt"
path_dump_files = "Lab 06\\poligon\\dump_files"
path_dump_files_B = "Lab 06\\poligon\\dump_files\\B.txt"

print(task1(path_lab6))

print(task2(path_poligon))

print(task3(path_poligon))

print(task4(path_sample4))

task5(path_sample5, [1, 2, 3, "--4"])

task6(path_dump_files)

task7(path_this, path_poligon)

task8(path_dump_files_B)