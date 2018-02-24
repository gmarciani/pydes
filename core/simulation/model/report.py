"""
Utility classes that realize reports for experiments.
"""


from collections import OrderedDict
from core.utils.file_utils import create_dir_tree
from core.utils.csv_utils import save


class SimpleReport(object):
    """
    The simplest report for an experiment.
    """

    def __init__(self, title):
        """
        Creates a new report.
        :param title: (string) the title of the report.
        """
        self.title = title
        self.params = OrderedDict()

    def add(self, section_title, param_title, param_value):
        """
        Adds a new parameter to the report.
        :param section_title: (string) the title of the section for the new
        parameter.
        :param param_title: (string) the name of the new parameter.
        :param param_value: (object) the value of the new parameter.
        :return: (void)
        """
        if section_title not in self.params:
            self.params[section_title] = []
        self.params[section_title].append((param_title, str(param_value)))

    def add_all(self, section_title, obj):
        """
        Add all object public attributes.
        :param section_title: (string) the title of the section for the new
        parameter.
        :param obj: the object to scan for attributes.
        :return: (void)
        """
        for attr in obj.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(obj, attr)):
                value = obj.__dict__[attr]
                if isinstance(value, float):
                    self.add(section_title, attr, round(value, 3))
                else:
                    self.add(section_title, attr, str(value))

    def add_all_attrs(self, section_title, obj, *attrs):
        """
        Add all object attributes.
        :param section_title: (string) the title of the section for the new
        parameter.
        :param obj: the object to scan for attributes.
        :param attrs: the attributes to add.
        :return: (void)
        """
        for attr in attrs:
            if attr in obj.__dict__ and not callable(getattr(obj, attr)):
                value = obj.__dict__[attr]
                if isinstance(value, float):
                    self.add(section_title, attr, round(value, 3))
                else:
                    self.add(section_title, attr, value)

    def get(self, section_title, param_title):
        """
        Retrieve the value of the given parameter.
        :param section_title: the title of the section.
        :param param_title: the name of the arameter.
        :return: the value of the parameter, if present; None, otherwise.
        """
        for elem in self.params[section_title]:
            if elem[0] == param_title:
                return elem[1]
        return None

    def save_txt(self, filename):
        """
        Save the report onto a file.
        :param filename: (string) the absolute file path.
        :return: (void)
        """
        create_dir_tree(filename)
        with open(filename, "w+") as f:
            f.write(str(self))

    def save_csv(self, filename, append=False, skip_header=False):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :return: None
        """
        header = ["name"]
        row = [self.title]

        for section in self.params:
            for p in self.params[section]:
                header.append("{}.{}".format(section, p[0]))
                row.append(p[1])
        data = [row]
        save(filename, header, data, append, skip_header)

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        title_separator = "=" * 50

        s = "\n{}\n{:^50}\n{}\n".format(title_separator, self.title, title_separator)

        for section in self.params.items():
            s += "\n{:^50}\n".format(section[0])
            for p in section[1]:
                s += "{:.<25}{:.>25}\n".format(str(p[0]), str(p[1]))

        return s