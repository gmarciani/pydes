"""
Utilities for CSV file management.
"""

from core.utils.file_utils import create_dir_tree


def save(filename, names, data, skip_header=False, append=False):
    """
    Save data as CSV.
    :param filename: (string) the filename.
    :param names: (list(string)) the list of names in header.
    :param data: (list(tuple)) the data.
    :param skip_header: (bool) if True, skip the CSV header.
    :param append: (bool) if True, append to an existing file.
    :return: None
    """
    create_dir_tree(filename)

    mode = "a" if append else "w+"

    with open(filename, mode) as f:
        if not skip_header:
            f.write(",".join(names))
            f.write("\n")

        for sample in data:
            f.write(",".join(map(str, sample)))
            f.write("\n")