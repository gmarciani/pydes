"""
Utilities for file system management.
"""

import errno
from os import path, makedirs


def create_dir_tree(filename):
    """
    Create directory trees.
    :param filename:
    :return: (void)
    """
    if not path.exists(path.dirname(filename)):
        try:
            makedirs(path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def save_list_of_numbers(filename, numbers):
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as resfile:
        for value in numbers:
            resfile.write(str(value) + "\n")


def append_list_of_numbers(filename, numbers):
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, "a") as resfile:
        for value in numbers:
            resfile.write(str(value) + "\n")


def save_list_of_pairs(filename, pairs):
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as resfile:
        for pair in pairs:
            resfile.write("{},{}\n".format(pair[0], pair[1]))


def append_list_of_pairs(filename, pairs):
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, "a") as resfile:
        for pair in pairs:
            resfile.write("{},{}\n".format(pair[0], pair[1]))


def save_csv(filename, list_dict):
    """
    Saves the report onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    save_header_csv(filename, list_dict)
    append_csv(filename, list_dict)


def save_header_csv(filename, list_dict):
    """
    Save report headers onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    with open(filename, "w+") as resfile:
        resfile.write(",".join(list_dict.keys()))
        resfile.write("\n")

def append_csv(filename, list_dict):
    """
    Append the report onto a CSV file.
    :param filename: (string) the absolute file path.
    :param list_dict: ([dict]) the list of dictionaries.
    :return: (void)
    """
    with open(filename, "a+") as resfile:
        resfile.write(",".join(list_dict.values()))
        resfile.write("\n")


if __name__ == "__main__":
    filename = "./test.txt"

    save_list_of_pairs(filename, [])
    l = [(1, 2)]
    append_list_of_pairs(filename, l)
    l = [(2, 4)]
    append_list_of_pairs(filename, l)
