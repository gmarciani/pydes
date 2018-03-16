"""
Utilities for CSV file management.
"""

from core.utils.file_utils import create_dir_tree, is_empty_file, empty_file


def save_csv(filename, names, data, append=False, skip_header=False, empty=False):
    """
    Save data as CSV.
    :param filename: (string) the filename.
    :param names: (list(string)) the list of names in header.
    :param data: (list(tuple)) the data.
    :param append: (bool) if True, append to an existing file.
    :param skip_header: (bool) if True, skip the CSV header.
    :param empty: (bool) if True, the file is emptied.
    :return: None
    """
    create_dir_tree(filename)

    if empty:
        empty_file(filename)

    mode = "a+" if append else "w+"

    with open(filename, mode) as f:
        if is_empty_file(filename) and not skip_header:
            f.write(",".join(map(str_csv, names)))
            f.write("\n")

        for sample in data:
            f.write(",".join(map(str, sample)))
            f.write("\n")


def str_csv(s):
    return s.lower().replace(" ", "_")