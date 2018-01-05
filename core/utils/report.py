"""
Utility classes that realize reports for experiments.
"""


from collections import OrderedDict
import os


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
        """
        if section_title not in self.params:
            self.params[section_title] = []
        self.params[section_title].append((param_title, param_value))

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

    def save(self, filename):
        """
        Saves the report onto a file.
        :param filename: (string) the absolute file path.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w+') as resfile:
            resfile.write(str(self))

    def __str__(self):
        title_separator = '=' * 60

        s = '\n{}\n{:^60}\n{}\n'.format(title_separator, self.title, title_separator)

        for section in self.params.items():
            s += '\n{:^60}\n'.format(section[0])
            for p in section[1]:
                s += '{:.<30}{:.>30}\n'.format(str(p[0]), str(p[1]))

        return s